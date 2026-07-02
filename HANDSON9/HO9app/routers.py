from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from jose import jwt, JWTError

# Correctly import the database module and schemas
import HO9app.database as db
from HO9app.security import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from HO9app.schemas import UserCreate, UserResponse, Token, CourseResponse
router = APIRouter()

# 92. Define the standard OAuth2 token extraction scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# =============================================================================
# TASK 1: USER REGISTRATION
# =============================================================================
@router.post("/api/v1/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate):
    for user in db.users_db.values(): # <-- Make sure "db." is written here!
        if user["email"] == user_in.email:
            raise HTTPException(status_code=409, detail="Email already registered")

            
    new_id = db.user_id_counter
    # 87 & 89. Hash plain password via secure slow bcrypt hashing algorithms
    hashed_pwd = get_password_hash(user_in.password)
    
    # 86. Build unique user mapping payload entry
    user_record = {
        "id": new_id,
        "email": user_in.email,
        "hashed_password": hashed_pwd,
        "is_active": True
    }
    
    db.users_db[new_id] = user_record
    db.user_id_counter += 1
    return user_record

# =============================================================================
# TASK 2: JWT LOGIN & PROTECTED DEPENDENCIES
# =============================================================================

@router.post("/api/v1/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_record = None
    for u in db.users_db.values():
        if u["email"] == form_data.username:
            user_record = u
            break
            
    # 91. Verify email and validate password hashes
    if not user_record or not verify_password(form_data.password, user_record["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
        
    # 91. Create access token with an expiry of 30 minutes
    access_token = create_access_token(data={"sub": user_record["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

# 92. get_current_user dependency helper to extract and decode token layers
async def get_current_user(token: str = Depends(oauth2_scheme)):
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise auth_exception
    except JWTError:
        raise auth_exception
        
    for user in db.users_db.values():
        if user["email"] == username:
            return user
            
    raise auth_exception

# =============================================================================
# SECURED APP MANAGEMENT PATHS
# =============================================================================

# Public Route: Does not require auth tokens
@router.get("/api/v1/courses/", response_model=List[CourseResponse])
async def get_courses():
    return list(db.courses_db.values())

# 93. Protected Route (POST): Requires a valid user token via dependency injection
@router.post("/api/v1/courses/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_secure_course(course: CourseResponse, current_user: dict = Depends(get_current_user)):
    if course.id in db.courses_db:
        raise HTTPException(status_code=400, detail="Course already exists")
    db.courses_db[course.id] = course.model_dump()
    return course

# 93. Protected Route (DELETE): Guarded via Depends(get_current_user)
@router.delete("/api/v1/courses/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_secure_course(id: int, current_user: dict = Depends(get_current_user)):
    if id not in db.courses_db:
        raise HTTPException(status_code=404, detail="Course record not found")
    del db.courses_db[id]
    return None
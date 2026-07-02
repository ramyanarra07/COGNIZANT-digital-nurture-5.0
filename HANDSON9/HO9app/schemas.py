from pydantic import BaseModel, EmailStr

# --- User Schemas (Step 86) ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

# --- Authentication Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- Course Schemas ---
class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from HO6app.database import get_db
from HO6app.models import Course, Department
from HO6app.schemas import CourseCreate, CourseResponse, DepartmentResponse

router = APIRouter(prefix="/api")

# --- Initialize Default Mock Seed Data ---
async def seed_data(db: AsyncSession):
    result = await db.execute(select(Department))
    if not result.scalars().first():
        d1 = Department(name="Computer Science")
        d2 = Department(name="Electrical Engineering")
        db.add_all([d1, d2])
        await db.commit()

# --- 60. Create Course Route (Async POST) ---
@router.post("/courses/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    # Verify target department exists
    dept_check = await db.execute(select(Department).filter(Department.id == course.department_id))
    if not dept_check.scalars().first():
        raise HTTPException(status_code=400, detail="Referenced Department ID does not exist")

    db_course = Course(**course.model_dump())
    db.add(db_course)
    await db.commit()          # 66. Async commit
    await db.refresh(db_course)
    return db_course

# --- 63 & 65. Paginated and Filtered Fetch Route (Async GET) ---
@router.get("/courses/", response_model=List[CourseResponse])
async def get_courses(
    skip: int = 0, 
    limit: int = 10, 
    department_id: Optional[int] = None, 
    db: AsyncSession = Depends(get_db)
):
    query = select(Course)
    if department_id is not None:
        query = query.filter(Course.department_id == department_id)
    
    # Apply offset (skip) and limit conditions
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())

# --- 62. Fetch by Path Parameter Route (Async GET) ---
@router.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course_by_id(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# Fetch Department with Nested Courses (Step 59 Verification)
@router.get("/departments/{dept_id}", response_model=DepartmentResponse)
async def get_department_details(dept_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department).filter(Department.id == dept_id))
    dept = result.scalars().first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept
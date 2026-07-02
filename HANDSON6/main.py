import uvicorn
from fastapi import FastAPI
from HO6app.database import engine, Base, async_session
from HO6app.routers import router, seed_data

# 57. Initialize the foundational application instance
app = FastAPI(title="Course Management API", version="1.0")

# Mount structural sub-routing configurations
app.include_router(router)

# Automated DB Schema generation on startup execution loops
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # Create database tables if they do not exist
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as session:
        await seed_data(session)

# 57. Base home-page validation route mapping
@app.get("/")
async def root():
    return {"message": "API running"}

if __name__ == "__main__":
    # 57. Run using Uvicorn server on default port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# Asynchronous SQLite connection string
DATABASE_URL = "sqlite+aiosqlite:///./handson6.db"

# 64. Set up the async engine and session factory
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# 64. Define get_db() dependency function yielding database sessions async
async def get_db():
    async with async_session() as session:
        yield session
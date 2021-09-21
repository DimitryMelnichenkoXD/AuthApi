from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
from auth_package import models

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://Zm2weJE6DHVYn4FORvIH:EbFsmImJl6rPbX3wsVUC@164.90.179.1:5432/db_test"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(models.Base.metadata.drop_all)
#         await conn.run_sync(models.Base.metadata.create_all)
#
#
# # Dependency
# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session

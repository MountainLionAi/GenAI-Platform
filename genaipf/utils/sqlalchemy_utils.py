import asyncio
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, func, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from genaipf.conf import db_conf

# Configuration
# DATABASE_URL = f"mysql+asyncmy://username:password@host:port/database_name"
DATABASE_URL = f"mysql+asyncmy://{db_conf.USER}:{db_conf.PASSWORD}@{db_conf.HOST}:{db_conf.PORT}/{db_conf.DATABASE}"

# Base class for models
Base = declarative_base()

# Create an async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Create a session maker bound to the engine
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def list_tables():
    async with AsyncSessionLocal() as session:
        # Formulate the raw SQL query to list tables
        result = await session.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        print("Tables in the database:")
        t_l = []
        for table in tables:
            t_l.append(table[0])
        return t_l



'''
conn = await engine.connect()
await conn.close()
'''
        
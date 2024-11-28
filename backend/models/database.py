import os
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

conn = "mysql+pymysql://{}:{}@{}/{}"
conn = conn.format(
    os.getenv("DB_USER"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_URL_ENDPOINT"),
    os.getenv("DB_SCHEMA"),
)

engine = create_engine(conn, pool_size=30, pool_recycle=1800, echo=False)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)

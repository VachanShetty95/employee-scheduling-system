import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute
from models.database import engine, init_db
from routes.routers import api_router
from sqlmodel import Session

from backend.models.seeding import prepopulate_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application has started...")
    init_db()
    logging.info("Database startup completed")
    with Session(engine) as session:
        logging.info("Loading dummy data")
        prepopulate_data(session=session)
    yield


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


API_V1_STR = os.getenv("API_V1_STR")

app = FastAPI(
    title=f"{os.getenv('PROJECT_NAME')}",
    openapi_url=f"{API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

app.include_router(api_router, prefix=API_V1_STR)

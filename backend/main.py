import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application has started...")
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

from fastapi import APIRouter
from routes import employees

from backend.routes import (
    locations,
    managers,
    production_lines,
    shifts,
    skills,
    time_off_requests,
)

api_router = APIRouter()
api_router.include_router(employees.router, prefix="/employees", tags=["Employees"])
api_router.include_router(managers.router, prefix="/managers", tags=["Managers"])
api_router.include_router(
    production_lines.router, prefix="/production_lines", tags=["Production Lines"]
)
api_router.include_router(
    time_off_requests.router, prefix="/time_off_requests", tags=["Time Off Requests"]
)
api_router.include_router(locations.router, prefix="/locations", tags=["Locations"])
api_router.include_router(skills.router, prefix="/skills", tags=["Skills"])
api_router.include_router(shifts.router, prefix="/shifts", tags=["Shifts"])
# api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])

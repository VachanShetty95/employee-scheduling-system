import random

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models.database import get_db
from models.models import Manager, ProductionLine
from models.schemas import ManagerCreate, ManagerResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from src.reporting import report_generation_api, predict_headcount_api

router = APIRouter()


@router.get("/", response_model=list[ManagerResponse])
def get_managers(session: Session = Depends(get_db)):
    managers = session.exec(select(Manager)).all()
    return managers


@router.post("/create", response_model=ManagerResponse)
def create_manager(manager: ManagerCreate, session: Session = Depends(get_db)):
    db_manager = Manager.model_validate(manager)
    try:
        session.add(db_manager)
        session.commit()
        session.refresh(db_manager)
        return db_manager
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Integrity error occurred." + str(e),
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred." + str(e),
        )


@router.get("/generate-report")
def generate_report(session: Session = Depends(get_db)):
    production_line = session.exec(select(ProductionLine)).first()
    text = report_generation_api(
        employees_needed=production_line.no_of_employees_needed,
        employees_attended=production_line.no_of_employees_attended,
        factory_output=random.randint(500, 600),
        factory_target=random.randint(550, 600),
    )

    return JSONResponse(
        content=text, status_code=200
    )


# @router.get("/forecast-report")
# def forecast_report(session: Session = Depends(get_db)):
#     production_line = session.exec(select(ProductionLine)).first()
#     text = report_generation_api(
#         employees_needed=production_line.no_of_employees_needed,
#         employees_attended=production_line.no_of_employees_attended,
#         factory_output=random.randint(500, 600),
#         factory_target=random.randint(550, 600),
#     )
    
#     headcount = predict_headcount_api(
#         report_content=text, next_week_target=random.randint(500, 600)
#     )

#     return JSONResponse(
#         content=headcount, status_code=200
#     )

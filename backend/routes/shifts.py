from fastapi import APIRouter, Depends, HTTPException, status
from models.database import get_db
from models.models import Availability, Employee, ShiftDetail
from models.schemas import SchedulingResponse, ShiftDetailCreate, ShiftDetailResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from src.schedule import shift_schedule

router = APIRouter()


@router.get("/", response_model=list[ShiftDetailResponse])
def get_shifts(session: Session = Depends(get_db)):
    shifts = session.exec(select(ShiftDetail)).all()
    return shifts


@router.post("/create", response_model=ShiftDetailResponse)
def create_shift(shift: ShiftDetailCreate, session: Session = Depends(get_db)):
    db_shift = ShiftDetail.model_validate(shift)
    try:
        session.add(db_shift)
        session.commit()
        session.refresh(db_shift)
        return db_shift
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


@router.post("/schedule", response_model=SchedulingResponse)
def schedule_shifts(session: Session = Depends(get_db)):
    employees = session.exec(select(Employee)).all()
    shifts = session.exec(select(ShiftDetail)).all()
    availability = session.exec(select(Availability)).all()

    assignments = shift_schedule(
        employees=employees, shifts=shifts, availability=availability
    )
    # assignments = employee_scheduling_with_constraints(employees=employees, shifts=shifts, skills=skills, shift_requirements=shift_requirements, availability=availability)
    return SchedulingResponse(assignments=assignments)

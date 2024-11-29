import logging

from fastapi import APIRouter, Depends, HTTPException, status
from models.database import get_db
from models.models import (
    Availability,
    Employee,
    ShiftDetail,
    ShiftSchedule,
    TimeOffRequest,
)
from models.schemas import (
    SchedulingResponse,
    ShiftDetailCreate,
    ShiftDetailResponse,
    TimeOffRequestCreate,
)
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from src.schedule import shift_schedule

router = APIRouter()


@router.get("/", response_model=list[ShiftDetailResponse])
def get_shifts(session: Session = Depends(get_db)):
    shifts = session.exec(select(ShiftDetail)).all()
    return shifts


# @router.get("/", response_model=list[ShiftSchedule])
# def get_shifts_per_employee(session:Session = Depends(get_db)):
#     shifts = session.exec


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

    return SchedulingResponse(assignments=assignments)


@router.post("/update-shifts/")
async def update_shifts(body: TimeOffRequestCreate, session: Session = Depends(get_db)):
    try:
        shift_detail = session.exec(
            select(ShiftDetail).where(ShiftDetail.employee_id == body.employee_id)
        ).first()
        time_off_requests = session.exec(
            select(TimeOffRequest).where(TimeOffRequest.employee_id == body.employee_id)
        ).first()

        shift_detail.shift_date = body.request_date

        if time_off_requests is None:
            time_off_requests.request_date = body.request_date
            time_off_requests.start_date = body.start_date
            time_off_requests.end_date = body.end_date
            time_off_requests.reason_for_absence = body.reason_for_absence
            time_off_requests.status = "Pending"
            time_off_requests.employee_id = body.employee_id

        session.add(shift_detail)
        session.add(time_off_requests)
        session.commit()
        session.refresh(shift_detail)
        session.refresh(time_off_requests)

        return "Data Updated"
    except Exception as e:
        logging.error(f"Time Off Request was not added: {e} ")

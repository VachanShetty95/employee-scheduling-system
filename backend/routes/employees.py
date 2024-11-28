from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from models.database import get_db
from models.models import Availability, Employee
from models.schemas import AvailabilityResponse, EmployeeCreate, EmployeeResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=list[EmployeeResponse])
def get_employees(session: Session = Depends(get_db)):
    employees = session.exec(select(Employee)).all()
    return employees


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, session: Session = Depends(get_db)):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.post("/create", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, session: Session = Depends(get_db)):
    try:
        db_employee = Employee.model_validate(employee)
        session.add(db_employee)
        session.commit()
        session.refresh(db_employee)
        return db_employee
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error: " + str(e),
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred: " + str(e),
        )


@router.get(
    "/employees/{employee_id}/availability", response_model=List[AvailabilityResponse]
)
async def get_employee_availability(
    employee_id: int, session: Session = Depends(get_db)
):
    return session.exec(
        select(Availability).where(Availability.employee_id == employee_id)
    ).all()


@router.delete("/delete/{employee_id}")
def delete_employee(employee_id: int, session: Session = Depends(get_db)):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    session.delete(employee)
    session.commit()
    return {"detail": "Employee deleted"}

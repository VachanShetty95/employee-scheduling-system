from datetime import date, datetime, time
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlmodel import SQLModel


# Location Models
class LocationBase(SQLModel):
    location_name: str
    address: str
    kommun: str
    zipcode: str
    country: str


class LocationCreate(LocationBase):
    manager_id: Optional[int] = None


class LocationResponse(LocationBase):
    id: int
    manager_id: Optional[int]


# Skill Models
class SkillBase(SQLModel):
    skill_name: str
    skills_description: Optional[str] = None


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: int
    created_at: datetime
    updated_at: datetime


# Role Models
class RoleBase(SQLModel):
    role_name: str
    role_description: Optional[str] = None


class RoleCreate(RoleBase):
    role_id: int


class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime


# Employee Models
class EmployeeBase(SQLModel):
    first_name: str
    last_name: str
    employee_email: EmailStr
    employee_role: Optional[str] = None
    employee_preference_days: Optional[List[str]] = None
    employee_preference_shifts: Optional[List[str]] = None
    shift_allocated: Optional[str] = None
    hire_date: datetime
    is_active: bool = True


class EmployeeCreate(EmployeeBase):
    role_id: Optional[int] = None
    location_id: Optional[int] = None


class EmployeeResponse(EmployeeBase):
    id: int
    role_id: Optional[int] = None
    location_id: Optional[int] = None


# Shift Details Models
class ShiftDetailBase(SQLModel):
    shift_week_day: Literal[
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]
    shift_date: date
    shift_start_time: time
    shift_end_time: time
    shift_desc: Optional[str] = None
    capacity: int = Field(..., ge=0)  # No negative values allowed
    current_employees: Optional[int] = None


class ShiftDetailCreate(ShiftDetailBase):
    manager_id: int
    location_id: int
    employee_id: int


class ShiftDetailResponse(ShiftDetailBase):
    id: int
    manager_id: int
    location_id: int


# Production Line Models
class ProductionLineBase(SQLModel):
    assignment_name: str
    no_of_employees_needed: int
    no_of_employees_attended: int = 0  # Default to 0


class ProductionLineCreate(ProductionLineBase):
    manager_id: int
    location_id: int
    shift_id: Optional[int] = None


class ProductionLineResponse(ProductionLineBase):
    id: int
    manager_id: int
    location_id: int
    shift_id: Optional[int] = None


# Shift Schedule Models
class ShiftScheduleBase(SQLModel):
    shift_date: date
    shift_name: str  # Renamed from shift_type


class ShiftScheduleCreate(ShiftScheduleBase):
    employee_id: int
    location_id: int


class ShiftScheduleResponse(ShiftScheduleBase):
    id: int
    employee_id: int
    location_id: int


# Availability Models
class AvailabilityBase(SQLModel):
    day_of_week: Literal[
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]
    date_of_week: date
    start_time: time
    end_time: time


class AvailabilityCreate(AvailabilityBase):
    employee_id: int


class AvailabilityResponse(AvailabilityBase):
    id: int
    employee_id: int


# Time Off Request Models
class TimeOffRequestBase(SQLModel):
    request_date: date
    start_date: date
    end_date: date
    status: Literal["Pending", "Approved", "Denied"]
    reason_for_absence: Optional[str] = None

    # @field_validator("end_date")
    # @classmethod
    # def check_dates(cls, end_date, values):
    #     start_date = values.("start_date")
    #     if start_date and start_date > end_date:
    #         raise ValueError("start_date must be earlier than or equal to end_date")
    #     return end_date


class TimeOffRequestCreate(TimeOffRequestBase):
    employee_id: int


class TimeOffRequestResponse(TimeOffRequestBase):
    id: int
    employee_id: int


# Employee Skills Models
class EmployeeSkillBase(SQLModel):
    skill_level: Literal["Beginner", "Intermediate", "Advanced"]


class EmployeeSkillCreate(EmployeeSkillBase):
    employee_id: int
    skill_id: int


class EmployeeSkillResponse(EmployeeSkillBase):
    id: int
    employee_id: int
    skill_id: int
    verified: bool
    last_verified_at: Optional[datetime] = None


# Manager Models
class ManagerBase(SQLModel):
    manager_role: str


class ManagerCreate(ManagerBase):
    pass


class ManagerResponse(ManagerBase):
    id: int


# Scheduling Response Model
class SchedulingAssignment(SQLModel):
    employee_id: int
    shift_id: int
    shift_date: datetime
    shift_desc: str
    shift_start_time: time
    shift_end_time: time
    shift_date: date
    assigned: bool  # Whether the employee was successfully assigned


class SchedulingResponse(SQLModel):
    assignments: List[SchedulingAssignment]

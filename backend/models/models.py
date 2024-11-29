from datetime import date, datetime, time
from typing import List, Optional

from sqlmodel import JSON, Column, Enum, Field, Relationship, SQLModel


# Location Table
class Location(SQLModel, table=True):
    __tablename__ = "locations"
    id: Optional[int] = Field(default=None, primary_key=True)
    location_name: str = Field(nullable=False)
    address: str = Field(nullable=False)
    kommun: str = Field(nullable=False)
    zipcode: str = Field(nullable=False)
    country: str = Field(nullable=False)
    manager_id: Optional[int] = Field(default=None, foreign_key="managers.id")

    # Relationships
    manager: Optional["Manager"] = Relationship(back_populates="locations")
    employees: List["Employee"] = Relationship(back_populates="location")
    shifts: List["ShiftDetail"] = Relationship(back_populates="location")
    shift_schedules: List["ShiftSchedule"] = Relationship(back_populates="location")
    production_lines: List["ProductionLine"] = Relationship(back_populates="location")


# Skills Table
class Skill(SQLModel, table=True):
    __tablename__ = "skills"
    id: Optional[int] = Field(default=None, primary_key=True)
    skill_name: str = Field(nullable=False)
    skills_description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    employee_skills: List["EmployeeSkill"] = Relationship(back_populates="skill")


# Role Table
class Role(SQLModel, table=True):
    __tablename__ = "roles"
    id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str = Field(nullable=False)
    role_description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    employees: List["Employee"] = Relationship(back_populates="role")


# Employee Table
class Employee(SQLModel, table=True):
    __tablename__ = "employees"
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    employee_email: str = Field(nullable=False, unique=False, index=True)
    employee_role: Optional[str] = Field(default=None)
    employee_preference_days: Optional[List[str]] = Field(
        default=None, sa_column=Column(JSON)
    )
    employee_preference_shifts: Optional[List[str]] = Field(
        default=None, sa_column=Column(JSON)
    )
    shift_allocated: Optional[str] = Field(default=None)
    employee_available_days: Optional[bool] = Field(default=None)
    hire_date: datetime = Field(nullable=False)
    is_active: bool = Field(default=True)

    # Foreign Keys
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")
    location_id: Optional[int] = Field(default=None, foreign_key="locations.id")

    # Relationships
    role: Optional[Role] = Relationship(back_populates="employees")
    location: Optional[Location] = Relationship(back_populates="employees")
    availability: List["Availability"] = Relationship(back_populates="employee")
    location: Optional[Location] = Relationship(back_populates="employees")
    time_off_requests: List["TimeOffRequest"] = Relationship(back_populates="employee")
    employee_skills: List["EmployeeSkill"] = Relationship(back_populates="employee")
    shift_schedules: List["ShiftSchedule"] = Relationship(back_populates="employee")


# Shift Details Table
class ShiftDetail(SQLModel, table=True):
    __tablename__ = "shift_details"
    id: Optional[int] = Field(default=None, primary_key=True)
    shift_week_day: str = Field(nullable=False)
    shift_date: datetime = Field(nullable=False)
    shift_start_time: time = Field(nullable=False)
    shift_end_time: time = Field(nullable=False)
    shift_desc: Optional[str] = Field(default=None)
    capacity: Optional[int] = Field(default=None)
    current_employees: Optional[int] = Field(default=None)

    # Foreign Keys
    manager_id: int = Field(foreign_key="managers.id")
    location_id: int = Field(foreign_key="locations.id")

    # Relationships
    location: Optional[Location] = Relationship(back_populates="shifts")
    manager: Optional["Manager"] = Relationship(back_populates="shifts")


# Production Line Table
class ProductionLine(SQLModel, table=True):
    __tablename__ = "production_lines"
    id: Optional[int] = Field(default=None, primary_key=True)
    assignment_name: str = Field(nullable=False)
    no_of_employees_needed: int = Field(nullable=False)
    no_of_employees_attended: Optional[int] = Field(default=None)

    # Foreign Keys
    manager_id: int = Field(foreign_key="managers.id")
    location_id: int = Field(foreign_key="locations.id")
    shift_id: Optional[int] = Field(default=None, foreign_key="shift_details.id")

    # Relationships
    manager: Optional["Manager"] = Relationship(back_populates="production_lines")
    location: Optional[Location] = Relationship(back_populates="production_lines")


# Shift Schedule Table
class ShiftSchedule(SQLModel, table=True):
    __tablename__ = "shift_schedules"
    id: Optional[int] = Field(default=None, primary_key=True)
    shift_date: date = Field(nullable=False)
    shift_type: str = Field(nullable=False)

    # Foreign Keys
    employee_id: int = Field(foreign_key="employees.id")
    location_id: int = Field(foreign_key="locations.id")

    # Relationships
    employee: Optional[Employee] = Relationship(back_populates="shift_schedules")
    location: Optional[Location] = Relationship(back_populates="shift_schedules")


# Availability Table
class Availability(SQLModel, table=True):
    __tablename__ = "availability"
    id: Optional[int] = Field(default=None, primary_key=True)
    day_of_week: str = Field(nullable=False)
    date_of_week: str = Field(nullable=False)
    start_time: time = Field(nullable=False)
    end_time: time = Field(nullable=False)

    # Foreign Keys
    employee_id: int = Field(foreign_key="employees.id")

    # Relationships
    employee: Optional[Employee] = Relationship(back_populates="availability")


# Time Off Requests Table
class TimeOffRequest(SQLModel, table=True):
    __tablename__ = "time_off_requests"
    id: Optional[int] = Field(default=None, primary_key=True)
    request_date: date = Field(nullable=False)
    start_date: date = Field(nullable=False)
    end_date: date = Field(nullable=False)
    status: str = Field(
        sa_column=Column(Enum("Pending", "Approved", "Denied", name="request_status"))
    )
    reason_for_absence: Optional[str] = Field(default=None)

    # Foreign Keys
    employee_id: int = Field(foreign_key="employees.id")

    # Relationships
    employee: Optional[Employee] = Relationship(back_populates="time_off_requests")


# Employee Skills Table
class EmployeeSkill(SQLModel, table=True):
    __tablename__ = "employee_skills"
    id: Optional[int] = Field(default=None, primary_key=True)
    skill_level: str = Field(
        sa_column=Column(
            Enum("Beginner", "Intermediate", "Advanced", name="skill_level_enum")
        )
    )

    # Foreign Keys
    employee_id: int = Field(foreign_key="employees.id")
    skill_id: int = Field(foreign_key="skills.id")

    # Relationships
    employee: Optional[Employee] = Relationship(back_populates="employee_skills")
    skill: Optional[Skill] = Relationship(back_populates="employee_skills")


# Manager Table
class Manager(SQLModel, table=True):
    __tablename__ = "managers"
    id: Optional[int] = Field(default=None, primary_key=True)
    manager_role: str = Field(nullable=False)

    # Relationships
    locations: List["Location"] = Relationship(back_populates="manager")
    shifts: List["ShiftDetail"] = Relationship(back_populates="manager")
    production_lines: List["ProductionLine"] = Relationship(back_populates="manager")

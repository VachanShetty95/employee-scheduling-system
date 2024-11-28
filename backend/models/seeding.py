import logging
from datetime import datetime, time

from models.models import (
    Availability,
    Employee,
    Location,
    Manager,
    ProductionLine,
    Role,
    ShiftDetail,
    Skill,
)
from models.schemas import (
    AvailabilityCreate,
    EmployeeCreate,
    LocationCreate,
    ManagerCreate,
    ProductionLineCreate,
    RoleCreate,
    ShiftDetailCreate,
    SkillCreate,
)
from sqlmodel import Session


def prepopulate_data(session: Session):
    """
    Function to prepopulate the required tables with dummy data.
    """
    # Prepopulate Locations
    locations_data = [
        LocationCreate(
            location_name="Headquarters",
            address="123 Vasagatan",
            kommun="Stockholm",
            zipcode="12345",
            country="Sweden",
            manager_id=None,
        ),
        LocationCreate(
            location_name="Factory 1",
            address="456 Gothenburg",
            kommun="Gothenburg",
            zipcode="67890",
            country="Sweden",
            manager_id=None,
        ),
    ]
    locations = [Location(**loc.model_dump()) for loc in locations_data]

    # Prepopulate Skills
    skills_data = [
        SkillCreate(
            skill_name="Welding", skills_description="Expertise in welding metal parts"
        ),
        SkillCreate(
            skill_name="Painting",
            skills_description="Experience with industrial spray painting",
        ),
    ]
    skills = [Skill(**skill.model_dump()) for skill in skills_data]

    # Prepopulate Roles
    roles_data = [
        RoleCreate(
            role_name="Operator", role_description="Handles machinery and equipment"
        ),
        RoleCreate(
            role_name="Supervisor", role_description="Supervises a team of operators"
        ),
    ]
    roles = [Role(**role.model_dump()) for role in roles_data]

    # Prepopulate Managers
    managers_data = [
        ManagerCreate(manager_role="Plant Manager"),
        ManagerCreate(manager_role="Shift Supervisor"),
    ]
    managers = [Manager(**manager.model_dump()) for manager in managers_data]

    # Prepopulate Employees
    employees_data = [
        EmployeeCreate(
            first_name="John",
            last_name="Doe",
            employee_email="johndoe@example.com",
            employee_role="Operator",
            hire_date=datetime(2024, 1, 15),
            is_active=True,
            role_id=1,
            location_id=1,
        ),
        EmployeeCreate(
            first_name="Jane",
            last_name="Smith",
            employee_email="janesmith@example.com",
            employee_role="Supervisor",
            hire_date=datetime(2023, 2, 20),
            is_active=True,
            role_id=2,
            location_id=2,
        ),
    ]
    employees = [Employee(**employee.model_dump()) for employee in employees_data]

    # Prepopulate Shift Details
    shifts_data = [
        ShiftDetailCreate(
            shift_week_day="Friday",
            shift_date=datetime(2024, 11, 29),
            shift_start_time=time(6, 0),
            shift_end_time=time(14, 0),
            shift_desc="Morning shift",
            capacity=10,
            manager_id=1,
            location_id=1,
        ),
        ShiftDetailCreate(
            shift_week_day="Saturday",
            shift_date=datetime(2024, 11, 30),
            shift_start_time=time(14, 0),
            shift_end_time=time(22, 0),
            shift_desc="Afternoon shift",
            capacity=8,
            manager_id=2,
            location_id=2,
        ),
    ]
    shifts = [ShiftDetail(**shift.model_dump()) for shift in shifts_data]

    # Prepopulate Production Lines
    production_lines_data = [
        ProductionLineCreate(
            assignment_name="Line A - Assembly",
            no_of_employees_needed=5,
            manager_id=1,
            location_id=1,
        ),
        ProductionLineCreate(
            assignment_name="Line B - Packaging",
            no_of_employees_needed=3,
            manager_id=2,
            location_id=2,
        ),
    ]
    production_lines = [
        ProductionLine(**line.model_dump()) for line in production_lines_data
    ]

    # Prepopulate Availability
    availability_data = [
        AvailabilityCreate(
            day_of_week="Friday",
            start_time=time(6, 0),
            end_time=time(14, 0),
            employee_id=1,  # John Doe
        ),
        AvailabilityCreate(
            day_of_week="Tuesday",
            start_time=time(16, 0),
            end_time=time(0, 0),
            employee_id=1,  # John Doe
        ),
        AvailabilityCreate(
            day_of_week="Saturday",
            start_time=time(14, 0),
            end_time=time(22, 0),
            employee_id=2,  # Jane Smith
        ),
        AvailabilityCreate(
            day_of_week="Tuesday",
            start_time=time(16, 0),
            end_time=time(0, 0),
            employee_id=2,  # Jane Smith
        ),
    ]
    availability = [Availability(**avail.model_dump()) for avail in availability_data]

    # Bulk insert all data
    session.add_all(locations)
    session.add_all(skills)
    session.add_all(roles)
    session.add_all(managers)
    session.add_all(employees)
    session.add_all(shifts)
    session.add_all(production_lines)
    session.add_all(availability)

    # Commit the session to save data to the database
    session.commit()
    logging.info("Dummy data prepopulated successfully.")

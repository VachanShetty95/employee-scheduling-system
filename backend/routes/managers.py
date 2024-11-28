from fastapi import APIRouter, Depends, HTTPException, status
from models.database import get_db
from models.models import Manager
from models.schemas import ManagerCreate, ManagerResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

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

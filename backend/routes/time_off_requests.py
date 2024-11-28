from fastapi import APIRouter, Depends, HTTPException, status
from models.database import get_db
from models.models import TimeOffRequest
from models.schemas import TimeOffRequestCreate, TimeOffRequestResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=list[TimeOffRequestResponse])
def get_time_off_requests(session: Session = Depends(get_db)):
    requests = session.exec(select(TimeOffRequest)).all()
    return requests


@router.post("/create", response_model=TimeOffRequestResponse)
def create_time_off_request(
    request: TimeOffRequestCreate, session: Session = Depends(get_db)
):
    db_request = TimeOffRequest.model_validate(request)
    try:
        session.add(db_request)
        session.commit()
        session.refresh(db_request)
        return db_request
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

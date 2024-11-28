from fastapi import APIRouter, Depends, HTTPException, status
from models.database import get_db
from models.models import Location
from models.schemas import LocationCreate, LocationResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=list[LocationResponse])
def get_locations(session: Session = Depends(get_db)):
    locations = session.exec(select(Location)).all()
    return locations


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int, session: Session = Depends(get_db)):
    location = session.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.post("/create", response_model=LocationResponse)
def create_location(location: LocationCreate, session: Session = Depends(get_db)):
    db_location = Location.model_validate(location)
    try:
        session.add(db_location)
        session.commit()
        session.refresh(db_location)
        return db_location
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


@router.delete("/delete/{location_id}")
def delete_location(location_id: int, session: Session = Depends(get_db)):
    location = session.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    session.delete(location)
    session.commit()
    return {"detail": "Location deleted"}

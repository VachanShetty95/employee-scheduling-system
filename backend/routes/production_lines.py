from fastapi import APIRouter, Depends, HTTPException, status
from models.database import get_db
from models.models import ProductionLine
from models.schemas import ProductionLineCreate, ProductionLineResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=list[ProductionLineResponse])
def get_production_lines(session: Session = Depends(get_db)):
    production_lines = session.exec(select(ProductionLine)).all()
    return production_lines


@router.post("/create", response_model=ProductionLineResponse)
def create_production_line(
    production_line: ProductionLineCreate, session: Session = Depends(get_db)
):
    db_production_line = ProductionLine.model_validate(production_line)
    try:
        session.add(db_production_line)
        session.commit()
        session.refresh(db_production_line)
        return db_production_line
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

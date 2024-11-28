from fastapi import APIRouter, Depends, HTTPException, status
from models.database import get_db
from models.models import Skill
from models.schemas import SkillCreate, SkillResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=list[SkillResponse])
def get_skills(session: Session = Depends(get_db)):
    skills = session.exec(select(Skill)).all()
    return skills


@router.post("/create", response_model=SkillResponse)
def create_skill(skill: SkillCreate, session: Session = Depends(get_db)):
    db_skill = Skill.model_validate(skill)
    try:
        session.add(db_skill)
        session.commit()
        session.refresh(db_skill)
        return db_skill
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

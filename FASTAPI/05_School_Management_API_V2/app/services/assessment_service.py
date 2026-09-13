from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessment import AssessmentModel
from app.models.assessment_result import AssessmentResultModel
from app.models.school_class import SchoolClassModel
from app.schemas.assessment import AssessmentCreate, AssessmentPatch, AssessmentType, AssessmentUpdate


def get_assessments(
    db: Session,
    class_id: int | None = None,
    assessment_type: AssessmentType | None = None,
    search: str | None = None,
    sort_order: str = "asc",
    limit: int = 20,
    offset: int = 0,
):

    statement = select(AssessmentModel)

    if class_id is not None:
        statement = statement.where(
            AssessmentModel.class_id == class_id
        )

    if assessment_type is not None:
        statement = statement.where(
            AssessmentModel.assessment_type == assessment_type.value
        )

    if search is not None and search.strip():
        search_term = f"%{search.strip()}%"
        statement = statement.where(
            AssessmentModel.title.ilike(search_term)
        )

    if sort_order == "desc":
        statement = statement.order_by(AssessmentModel.due_date.desc())
    else:
        statement = statement.order_by(AssessmentModel.due_date.asc())

    statement = statement.offset(offset).limit(limit)

    return db.scalars(statement).all()


def get_assessment(db: Session, assessment_id: int):

    assessment = db.get(AssessmentModel, assessment_id)

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    return assessment


def create_assessment(db: Session, assessment: AssessmentCreate):

    school_class = db.get(SchoolClassModel, assessment.class_id)
    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    new_assessment = AssessmentModel(
        class_id=assessment.class_id,
        title=assessment.title,
        assessment_type=assessment.assessment_type.value,
        max_score=assessment.max_score,
        due_date=assessment.due_date
    )

    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    return new_assessment


def update_assessment(db: Session, assessment_id: int, updated_assessment: AssessmentUpdate):

    assessment = get_assessment(db, assessment_id)

    school_class = db.get(SchoolClassModel, updated_assessment.class_id)
    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    assessment.class_id = updated_assessment.class_id
    assessment.title = updated_assessment.title
    assessment.assessment_type = updated_assessment.assessment_type.value
    assessment.max_score = updated_assessment.max_score
    assessment.due_date = updated_assessment.due_date

    db.commit()
    db.refresh(assessment)

    return assessment


def patch_assessment(db: Session, assessment_id: int, updated_assessment: AssessmentPatch):

    assessment = get_assessment(db, assessment_id)

    if updated_assessment.class_id is not None:
        school_class = db.get(SchoolClassModel, updated_assessment.class_id)
        if school_class is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
        assessment.class_id = updated_assessment.class_id

    if updated_assessment.title is not None:
        assessment.title = updated_assessment.title

    if updated_assessment.assessment_type is not None:
        assessment.assessment_type = updated_assessment.assessment_type.value

    if updated_assessment.max_score is not None:
        if any(
            result.score > updated_assessment.max_score
            for result in assessment.results
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot lower max_score below an existing student result"
            )
        assessment.max_score = updated_assessment.max_score

    if updated_assessment.due_date is not None:
        assessment.due_date = updated_assessment.due_date

    db.commit()
    db.refresh(assessment)

    return assessment


def delete_assessment(db: Session, assessment_id: int):

    assessment = get_assessment(db, assessment_id)

    db.delete(assessment)
    db.commit()

    return


def get_class_assessments(db: Session, class_id: int):

    school_class = db.get(SchoolClassModel, class_id)
    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    statement = select(AssessmentModel).where(
        AssessmentModel.class_id == class_id
    ).order_by(AssessmentModel.due_date)

    return db.scalars(statement).all()

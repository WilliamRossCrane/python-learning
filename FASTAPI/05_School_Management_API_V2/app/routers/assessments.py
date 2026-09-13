from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.assessment import AssessmentModel
from app.models.school_class import SchoolClassModel
from app.schemas.assessment import (
    Assessment,
    AssessmentCreate,
    AssessmentUpdate
)


router = APIRouter(
    prefix="/api/v1/assessments",
    tags=["Assessments"]
)


@router.get(
    "/",
    response_model=list[Assessment]
)
def get_assessments(
    db: Session = Depends(get_db)
):

    statement = select(
        AssessmentModel
    ).order_by(
        AssessmentModel.due_date
    )

    assessments = db.scalars(
        statement
    ).all()

    return assessments


@router.get(
    "/{assessment_id}",
    response_model=Assessment
)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db)
):

    assessment = db.get(
        AssessmentModel,
        assessment_id
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    return assessment


@router.post(
    "/",
    response_model=Assessment,
    status_code=status.HTTP_201_CREATED
)
def create_assessment(
    assessment: AssessmentCreate,
    db: Session = Depends(get_db)
):

    school_class = db.get(
        SchoolClassModel,
        assessment.class_id
    )

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


@router.put(
    "/{assessment_id}",
    response_model=Assessment
)
def update_assessment(
    assessment_id: int,
    updated_assessment: AssessmentUpdate,
    db: Session = Depends(get_db)
):

    assessment = db.get(
        AssessmentModel,
        assessment_id
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    school_class = db.get(
        SchoolClassModel,
        updated_assessment.class_id
    )

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


@router.delete(
    "/{assessment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_assessment(
    assessment_id: int,
    db: Session = Depends(get_db)
):

    assessment = db.get(
        AssessmentModel,
        assessment_id
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    db.delete(assessment)
    db.commit()

    return


@router.get(
    "/classes/{class_id}/assessments",
    response_model=list[Assessment]
)
def get_class_assessments(
    class_id: int,
    db: Session = Depends(get_db)
):

    school_class = db.get(
        SchoolClassModel,
        class_id
    )

    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    statement = select(
        AssessmentModel
    ).where(
        AssessmentModel.class_id == class_id
    ).order_by(
        AssessmentModel.due_date
    )

    assessments = db.scalars(
        statement
    ).all()

    return assessments
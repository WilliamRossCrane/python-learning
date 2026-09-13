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
from app.models.assessment_result import AssessmentResultModel
from app.models.student import StudentModel
from app.schemas.assessment_result import (
    AssessmentResult,
    AssessmentResultCreate,
    AssessmentResultUpdate
)


router = APIRouter(
    prefix="/api/v1/results",
    tags=["Assessment Results"]
)


@router.get(
    "/",
    response_model=list[AssessmentResult]
)
def get_results(
    db: Session = Depends(get_db)
):

    statement = select(
        AssessmentResultModel
    )

    results = db.scalars(
        statement
    ).all()

    return results


@router.get(
    "/{result_id}",
    response_model=AssessmentResult
)
def get_result(
    result_id: int,
    db: Session = Depends(get_db)
):

    result = db.get(
        AssessmentResultModel,
        result_id
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment result not found"
        )

    return result


@router.post(
    "/",
    response_model=AssessmentResult,
    status_code=status.HTTP_201_CREATED
)
def create_result(
    result: AssessmentResultCreate,
    db: Session = Depends(get_db)
):

    assessment = db.get(
        AssessmentModel,
        result.assessment_id
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    student = db.get(
        StudentModel,
        result.student_id
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    if student not in assessment.school_class.students:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is not enrolled in the assessment's class"
        )

    if result.score > assessment.max_score:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Score cannot exceed maximum score of {assessment.max_score}"
        )

    duplicate_statement = select(
        AssessmentResultModel
    ).where(
        AssessmentResultModel.assessment_id == result.assessment_id,
        AssessmentResultModel.student_id == result.student_id
    )

    existing_result = db.scalar(
        duplicate_statement
    )

    if existing_result is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A result already exists for this student and assessment"
        )

    new_result = AssessmentResultModel(
        assessment_id=result.assessment_id,
        student_id=result.student_id,
        score=result.score
    )

    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return new_result


@router.put(
    "/{result_id}",
    response_model=AssessmentResult
)
def update_result(
    result_id: int,
    updated_result: AssessmentResultUpdate,
    db: Session = Depends(get_db)
):

    result = db.get(
        AssessmentResultModel,
        result_id
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment result not found"
        )

    assessment = db.get(
        AssessmentModel,
        result.assessment_id
    )

    if updated_result.score > assessment.max_score:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Score cannot exceed maximum score of {assessment.max_score}"
        )

    result.score = updated_result.score

    db.commit()
    db.refresh(result)

    return result


@router.delete(
    "/{result_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_result(
    result_id: int,
    db: Session = Depends(get_db)
):

    result = db.get(
        AssessmentResultModel,
        result_id
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment result not found"
        )

    db.delete(result)
    db.commit()

    return


@router.get(
    "/assessments/{assessment_id}/results",
    response_model=list[AssessmentResult]
)
def get_assessment_results(
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

    statement = select(
        AssessmentResultModel
    ).where(
        AssessmentResultModel.assessment_id == assessment_id
    )

    results = db.scalars(
        statement
    ).all()

    return results


@router.get(
    "/students/{student_id}/results",
    response_model=list[AssessmentResult]
)
def get_student_results(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.get(
        StudentModel,
        student_id
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    statement = select(
        AssessmentResultModel
    ).where(
        AssessmentResultModel.student_id == student_id
    )

    results = db.scalars(
        statement
    ).all()

    return results

@router.get(
    "/{result_id}/summary"
)
def get_result_summary(
    result_id: int,
    db: Session = Depends(get_db)
):

    result = db.get(
        AssessmentResultModel,
        result_id
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment result not found"
        )

    assessment = result.assessment
    student = result.student

    percentage = (
        result.score
        /
        assessment.max_score
    ) * 100

    return {
        "result_id": result.id,
        "student": {
            "id": student.id,
            "name": f"{student.first_name} {student.last_name}"
        },
        "assessment": {
            "id": assessment.id,
            "title": assessment.title
        },
        "score": result.score,
        "max_score": assessment.max_score,
        "percentage": round(
            percentage,
            2
        )
    }
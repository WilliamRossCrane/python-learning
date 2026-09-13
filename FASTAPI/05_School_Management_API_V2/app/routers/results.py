from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)

from sqlalchemy import func, select
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
    student_id: int | None = Query(default=None, gt=0),
    assessment_id: int | None = Query(default=None, gt=0),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):

    statement = select(
        AssessmentResultModel
    )

    if student_id is not None:
        statement = statement.where(
            AssessmentResultModel.student_id == student_id
        )

    if assessment_id is not None:
        statement = statement.where(
            AssessmentResultModel.assessment_id == assessment_id
        )

    statement = statement.order_by(
        AssessmentResultModel.id.asc()
    ).offset(offset).limit(limit)

    return db.scalars(statement).all()


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


@router.get(
    "/summary"
)
def get_results_summary(
    student_id: int | None = Query(default=None, gt=0),
    assessment_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db)
):

    statement = select(
        AssessmentResultModel
    )

    if student_id is not None:
        statement = statement.where(
            AssessmentResultModel.student_id == student_id
        )

    if assessment_id is not None:
        statement = statement.where(
            AssessmentResultModel.assessment_id == assessment_id
        )

    results = db.scalars(statement).all()

    if not results:
        return {
            "total_results": 0,
            "average_score": 0,
            "highest_score": 0,
            "lowest_score": 0
        }

    scores = [result.score for result in results]

    return {
        "total_results": len(results),
        "average_score": round(sum(scores) / len(scores), 2),
        "highest_score": max(scores),
        "lowest_score": min(scores)
    }


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

    if result.score > assessment.max_score:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Score cannot exceed maximum score of {assessment.max_score}"
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

    existing_result = db.scalar(
        select(AssessmentResultModel).where(
            AssessmentResultModel.assessment_id == result.assessment_id,
            AssessmentResultModel.student_id == result.student_id
        )
    )

    if existing_result is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A result for this student and assessment already exists"
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
    updated_result: AssessmentResultCreate,
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
        updated_result.assessment_id
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    if updated_result.score > assessment.max_score:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Score cannot exceed maximum score of {assessment.max_score}"
        )

    student = db.get(
        StudentModel,
        updated_result.student_id
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    duplicate = db.scalar(
        select(AssessmentResultModel).where(
            AssessmentResultModel.assessment_id == updated_result.assessment_id,
            AssessmentResultModel.student_id == updated_result.student_id,
            AssessmentResultModel.id != result_id
        )
    )

    if duplicate is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A result for this student and assessment already exists"
        )

    result.assessment_id = updated_result.assessment_id
    result.student_id = updated_result.student_id
    result.score = updated_result.score

    db.commit()
    db.refresh(result)

    return result


@router.patch(
    "/{result_id}",
    response_model=AssessmentResult
)
def patch_result(
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
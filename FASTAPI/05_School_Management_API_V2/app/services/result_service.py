from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessment import AssessmentModel
from app.models.assessment_result import AssessmentResultModel
from app.models.student import StudentModel
from app.schemas.assessment_result import AssessmentResultCreate, AssessmentResultUpdate


def get_results(
    db: Session,
    student_id: int | None = None,
    assessment_id: int | None = None,
    limit: int = 20,
    offset: int = 0,
):

    statement = select(AssessmentResultModel)

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


def get_result(db: Session, result_id: int):

    result = db.get(AssessmentResultModel, result_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment result not found"
        )

    return result


def get_results_summary(db: Session, student_id: int | None = None, assessment_id: int | None = None):

    statement = select(AssessmentResultModel)

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


def create_result(db: Session, result: AssessmentResultCreate):

    assessment = db.get(AssessmentModel, result.assessment_id)
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    student = db.get(StudentModel, result.student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    if result.score > assessment.max_score:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Score cannot exceed maximum score of {assessment.max_score}"
        )

    if student not in assessment.school_class.students:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is not enrolled in the assessment class"
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


def update_result(db: Session, result_id: int, updated_result: AssessmentResultCreate):

    result = get_result(db, result_id)

    assessment = db.get(AssessmentModel, updated_result.assessment_id)
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    student = db.get(StudentModel, updated_result.student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    if updated_result.score > assessment.max_score:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Score cannot exceed maximum score of {assessment.max_score}"
        )

    if student not in assessment.school_class.students:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is not enrolled in the assessment class"
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


def patch_result(db: Session, result_id: int, updated_result: AssessmentResultUpdate):

    result = get_result(db, result_id)

    assessment = db.get(AssessmentModel, result.assessment_id)
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

    result.score = updated_result.score

    db.commit()
    db.refresh(result)

    return result


def delete_result(db: Session, result_id: int):

    result = get_result(db, result_id)

    db.delete(result)
    db.commit()

    return

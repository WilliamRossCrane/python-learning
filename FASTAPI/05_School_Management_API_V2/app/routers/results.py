from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.assessment_result import (
    AssessmentResult,
    AssessmentResultCreate,
    AssessmentResultUpdate
)
from app.services.result_service import (
    create_result as create_result_service,
    delete_result as delete_result_service,
    get_result as get_result_service,
    get_results as get_results_service,
    get_results_summary as get_results_summary_service,
    patch_result as patch_result_service,
    update_result as update_result_service,
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

    return get_results_service(db=db, student_id=student_id, assessment_id=assessment_id, limit=limit, offset=offset)


@router.get(
    "/{result_id}",
    response_model=AssessmentResult
)
def get_result(
    result_id: int,
    db: Session = Depends(get_db)
):

    return get_result_service(db=db, result_id=result_id)


@router.get(
    "/summary"
)
def get_results_summary(
    student_id: int | None = Query(default=None, gt=0),
    assessment_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db)
):

    return get_results_summary_service(db=db, student_id=student_id, assessment_id=assessment_id)


@router.post(
    "/",
    response_model=AssessmentResult,
    status_code=status.HTTP_201_CREATED
)
def create_result(
    result: AssessmentResultCreate,
    db: Session = Depends(get_db)
):

    return create_result_service(db=db, result=result)


@router.put(
    "/{result_id}",
    response_model=AssessmentResult
)
def update_result(
    result_id: int,
    updated_result: AssessmentResultCreate,
    db: Session = Depends(get_db)
):

    return update_result_service(db=db, result_id=result_id, updated_result=updated_result)


@router.patch(
    "/{result_id}",
    response_model=AssessmentResult
)
def patch_result(
    result_id: int,
    updated_result: AssessmentResultUpdate,
    db: Session = Depends(get_db)
):

    return patch_result_service(db=db, result_id=result_id, updated_result=updated_result)


@router.delete(
    "/{result_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_result(
    result_id: int,
    db: Session = Depends(get_db)
):

    delete_result_service(db=db, result_id=result_id)
    return
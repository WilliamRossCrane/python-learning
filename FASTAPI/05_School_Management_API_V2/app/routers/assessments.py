from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.assessment import (
    Assessment,
    AssessmentCreate,
    AssessmentType,
    AssessmentUpdate
)
from app.services.assessment_service import (
    create_assessment as create_assessment_service,
    delete_assessment as delete_assessment_service,
    get_assessment as get_assessment_service,
    get_assessments as get_assessments_service,
    get_class_assessments as get_class_assessments_service,
    update_assessment as update_assessment_service,
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
    class_id: int | None = Query(default=None, gt=0),
    assessment_type: AssessmentType | None = Query(default=None),
    search: str | None = Query(default=None),
    sort_order: str = Query(default="asc", pattern="^(asc|desc)$"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):

    return get_assessments_service(
        db=db,
        class_id=class_id,
        assessment_type=assessment_type,
        search=search,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{assessment_id}",
    response_model=Assessment
)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db)
):

    return get_assessment_service(db=db, assessment_id=assessment_id)


@router.post(
    "/",
    response_model=Assessment,
    status_code=status.HTTP_201_CREATED
)
def create_assessment(
    assessment: AssessmentCreate,
    db: Session = Depends(get_db)
):

    return create_assessment_service(db=db, assessment=assessment)


@router.put(
    "/{assessment_id}",
    response_model=Assessment
)
def update_assessment(
    assessment_id: int,
    updated_assessment: AssessmentUpdate,
    db: Session = Depends(get_db)
):

    return update_assessment_service(db=db, assessment_id=assessment_id, updated_assessment=updated_assessment)


@router.delete(
    "/{assessment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_assessment(
    assessment_id: int,
    db: Session = Depends(get_db)
):

    delete_assessment_service(db=db, assessment_id=assessment_id)
    return


@router.get(
    "/classes/{class_id}/assessments",
    response_model=list[Assessment]
)
def get_class_assessments(
    class_id: int,
    db: Session = Depends(get_db)
):

    return get_class_assessments_service(db=db, class_id=class_id)
from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.school_class import (
    SchoolClass,
    SchoolClassCreate,
    SchoolClassUpdate
)
from app.services.class_service import (
    create_class as create_class_service,
    delete_class as delete_class_service,
    get_class as get_class_service,
    get_classes as get_classes_service,
    update_class as update_class_service,
)


router = APIRouter(
    prefix="/api/v1/classes",
    tags=["Classes"]
)


@router.get(
    "/",
    response_model=list[SchoolClass]
)
def get_classes(
    teacher_id: int | None = Query(default=None, gt=0),
    subject_id: int | None = Query(default=None, gt=0),
    search: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):

    return get_classes_service(
        db=db,
        teacher_id=teacher_id,
        subject_id=subject_id,
        search=search,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{class_id}",
    response_model=SchoolClass
)
def get_class(
    class_id: int,
    db: Session = Depends(get_db)
):

    return get_class_service(db=db, class_id=class_id)


@router.post(
    "/",
    response_model=SchoolClass,
    status_code=status.HTTP_201_CREATED
)
def create_class(
    school_class: SchoolClassCreate,
    db: Session = Depends(get_db)
):

    return create_class_service(db=db, school_class=school_class)


@router.put(
    "/{class_id}",
    response_model=SchoolClass
)
def update_class(
    class_id: int,
    updated_class: SchoolClassUpdate,
    db: Session = Depends(get_db)
):

    return update_class_service(db=db, class_id=class_id, updated_class=updated_class)


@router.delete(
    "/{class_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_class(
    class_id: int,
    db: Session = Depends(get_db)
):

    delete_class_service(db=db, class_id=class_id)
    return
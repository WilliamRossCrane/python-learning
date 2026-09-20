from fastapi import (
    APIRouter,
    Depends,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.teacher import (
    Teacher,
    TeacherCreate,
    TeacherPatch,
    TeacherUpdate
)
from app.services.teacher_service import (
    create_teacher as create_teacher_service,
    delete_teacher as delete_teacher_service,
    get_teacher as get_teacher_service,
    get_teachers as get_teachers_service,
    patch_teacher as patch_teacher_service,
    update_teacher as update_teacher_service,
)


router = APIRouter(
    prefix="/api/v1/teachers",
    tags=["Teachers"]
)


@router.get(
    "/",
    response_model=list[Teacher]
)
def get_teachers(
    db: Session = Depends(get_db)
):

    return get_teachers_service(db=db)


@router.get(
    "/{teacher_id}",
    response_model=Teacher
)
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):

    return get_teacher_service(db=db, teacher_id=teacher_id)


@router.post(
    "/",
    response_model=Teacher,
    status_code=status.HTTP_201_CREATED
)
def create_teacher(
    teacher: TeacherCreate,
    db: Session = Depends(get_db)
):

    return create_teacher_service(db=db, teacher=teacher)


@router.put(
    "/{teacher_id}",
    response_model=Teacher
)
def update_teacher(
    teacher_id: int,
    updated_teacher: TeacherUpdate,
    db: Session = Depends(get_db)
):

    return update_teacher_service(db=db, teacher_id=teacher_id, updated_teacher=updated_teacher)


@router.patch(
    "/{teacher_id}",
    response_model=Teacher
)
def patch_teacher(
    teacher_id: int,
    updated_teacher: TeacherPatch,
    db: Session = Depends(get_db)
):

    return patch_teacher_service(db=db, teacher_id=teacher_id, updated_teacher=updated_teacher)


@router.delete(
    "/{teacher_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):

    delete_teacher_service(db=db, teacher_id=teacher_id)
    return
from fastapi import APIRouter, HTTPException, status

from app.schemas.school_class import (
    SchoolClass,
    SchoolClassCreate,
    SchoolClassUpdate
)

from app.routers.students import students
from app.routers.teachers import teachers
from app.routers.subjects import subjects


router = APIRouter(
    prefix="/api/v1/classes",
    tags=["Classes"]
)


classes = [
    {
        "id": 1,
        "name": "Year 10 Business",
        "teacher_id": 1,
        "subject_id": 2,
        "student_ids": [1, 2]
    }
]


def teacher_exists(teacher_id: int):
    return any(
        teacher["id"] == teacher_id
        for teacher in teachers
    )


def subject_exists(subject_id: int):
    return any(
        subject["id"] == subject_id
        for subject in subjects
    )


def students_exist(student_ids: list[int]):
    existing_student_ids = {
        student["id"]
        for student in students
    }

    return all(
        student_id in existing_student_ids
        for student_id in student_ids
    )


@router.get("/", response_model=list[SchoolClass])
def get_classes():
    return classes


@router.get("/{class_id}", response_model=SchoolClass)
def get_class(class_id: int):

    for school_class in classes:
        if school_class["id"] == class_id:
            return school_class

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Class not found"
    )


@router.post(
    "/",
    response_model=SchoolClass,
    status_code=status.HTTP_201_CREATED
)
def create_class(school_class: SchoolClassCreate):

    if not teacher_exists(school_class.teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    if not subject_exists(school_class.subject_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

    if not students_exist(school_class.student_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more students were not found"
        )

    new_id = max(
        existing_class["id"]
        for existing_class in classes
    ) + 1 if classes else 1

    new_class = {
        "id": new_id,
        **school_class.model_dump()
    }

    classes.append(new_class)

    return new_class


@router.put("/{class_id}", response_model=SchoolClass)
def update_class(
    class_id: int,
    updated_class: SchoolClassUpdate
):

    if not teacher_exists(updated_class.teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    if not subject_exists(updated_class.subject_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

    if not students_exist(updated_class.student_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more students were not found"
        )

    for index, school_class in enumerate(classes):

        if school_class["id"] == class_id:

            classes[index] = {
                "id": class_id,
                **updated_class.model_dump()
            }

            return classes[index]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Class not found"
    )


@router.delete(
    "/{class_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_class(class_id: int):

    for index, school_class in enumerate(classes):

        if school_class["id"] == class_id:
            classes.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Class not found"
    )
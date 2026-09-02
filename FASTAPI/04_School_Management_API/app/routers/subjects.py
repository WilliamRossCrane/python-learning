from fastapi import APIRouter, HTTPException, status

from app.schemas.subject import Subject, SubjectCreate, SubjectUpdate


router = APIRouter(
    prefix="/api/v1/subjects",
    tags=["Subjects"]
)


subjects = [
    {
        "id": 1,
        "name": "Digital Solutions",
        "code": "DIG",
        "description": "Senior secondary Digital Solutions"
    },
    {
        "id": 2,
        "name": "Business",
        "code": "BUS",
        "description": "Secondary Business studies"
    }
]


@router.get("/", response_model=list[Subject])
def get_subjects():
    return subjects


@router.get("/{subject_id}", response_model=Subject)
def get_subject(subject_id: int):

    for subject in subjects:
        if subject["id"] == subject_id:
            return subject

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Subject not found"
    )


@router.post(
    "/",
    response_model=Subject,
    status_code=status.HTTP_201_CREATED
)
def create_subject(subject: SubjectCreate):

    for existing_subject in subjects:
        if existing_subject["code"].lower() == subject.code.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A subject with this code already exists"
            )

    new_id = max(
        existing_subject["id"]
        for existing_subject in subjects
    ) + 1 if subjects else 1

    new_subject = {
        "id": new_id,
        **subject.model_dump()
    }

    subjects.append(new_subject)

    return new_subject


@router.put("/{subject_id}", response_model=Subject)
def update_subject(
    subject_id: int,
    updated_subject: SubjectUpdate
):

    for index, subject in enumerate(subjects):

        if subject["id"] == subject_id:

            for existing_subject in subjects:
                if (
                    existing_subject["id"] != subject_id
                    and existing_subject["code"].lower()
                    == updated_subject.code.lower()
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="A subject with this code already exists"
                    )

            subjects[index] = {
                "id": subject_id,
                **updated_subject.model_dump()
            }

            return subjects[index]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Subject not found"
    )


@router.delete(
    "/{subject_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_subject(subject_id: int):

    for index, subject in enumerate(subjects):

        if subject["id"] == subject_id:
            subjects.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Subject not found"
    )
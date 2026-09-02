from fastapi import APIRouter, HTTPException, status

from app.schemas.assessment import (
    Assessment,
    AssessmentCreate,
    AssessmentUpdate
)

from app.routers.classes import classes


router = APIRouter(
    prefix="/api/v1/assessments",
    tags=["Assessments"]
)


assessments = [
    {
        "id": 1,
        "class_id": 1,
        "title": "Business Lifecycle Exam",
        "assessment_type": "exam",
        "max_score": 100,
        "due_date": "2026-09-20"
    }
]


def class_exists(class_id: int):
    return any(
        school_class["id"] == class_id
        for school_class in classes
    )


@router.get("/", response_model=list[Assessment])
def get_assessments():
    return assessments


@router.get("/{assessment_id}", response_model=Assessment)
def get_assessment(assessment_id: int):

    for assessment in assessments:
        if assessment["id"] == assessment_id:
            return assessment

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Assessment not found"
    )


@router.get(
    "/class/{class_id}",
    response_model=list[Assessment]
)
def get_class_assessments(class_id: int):

    if not class_exists(class_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    return [
        assessment
        for assessment in assessments
        if assessment["class_id"] == class_id
    ]


@router.post(
    "/",
    response_model=Assessment,
    status_code=status.HTTP_201_CREATED
)
def create_assessment(assessment: AssessmentCreate):

    if not class_exists(assessment.class_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    new_id = max(
        existing_assessment["id"]
        for existing_assessment in assessments
    ) + 1 if assessments else 1

    new_assessment = {
        "id": new_id,
        **assessment.model_dump()
    }

    assessments.append(new_assessment)

    return new_assessment


@router.put(
    "/{assessment_id}",
    response_model=Assessment
)
def update_assessment(
    assessment_id: int,
    updated_assessment: AssessmentUpdate
):

    if not class_exists(updated_assessment.class_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    for index, assessment in enumerate(assessments):

        if assessment["id"] == assessment_id:

            assessments[index] = {
                "id": assessment_id,
                **updated_assessment.model_dump()
            }

            return assessments[index]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Assessment not found"
    )


@router.delete(
    "/{assessment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_assessment(assessment_id: int):

    for index, assessment in enumerate(assessments):

        if assessment["id"] == assessment_id:
            assessments.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Assessment not found"
    )
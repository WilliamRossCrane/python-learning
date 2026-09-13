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
import time
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks


router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Background Tasks"]
)


def write_audit_log(message: str):

    time.sleep(3)

    with open("audit_log.txt", "a") as file:
        file.write(
            f"{datetime.now().isoformat()} - {message}\n"
        )


@router.post("/audit")
def create_audit_task(
    message: str,
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(
        write_audit_log,
        message
    )

    return {
        "message": "Audit log task started",
        "status": "accepted"
    }
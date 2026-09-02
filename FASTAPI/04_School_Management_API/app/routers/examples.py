import asyncio
import time

from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1/examples",
    tags=["Examples"]
)


@router.get("/sync")
def sync_example():

    start_time = time.perf_counter()

    time.sleep(5)

    end_time = time.perf_counter()

    return {
        "type": "synchronous",
        "message": "Sync task finished",
        "duration": round(end_time - start_time, 2)
    }


@router.get("/async")
async def async_example():

    start_time = time.perf_counter()

    await asyncio.sleep(5)

    end_time = time.perf_counter()

    return {
        "type": "asynchronous",
        "message": "Async task finished",
        "duration": round(end_time - start_time, 2)
    }

async def fake_weather_request():
    await asyncio.sleep(2)

    return {
        "temperature": 27,
        "condition": "Sunny"
    }


async def fake_attendance_request():
    await asyncio.sleep(2)

    return {
        "present": 24,
        "absent": 2
    }


async def fake_assessment_request():
    await asyncio.sleep(2)

    return {
        "upcoming_assessments": 3
    }


@router.get("/async-dashboard")
async def async_dashboard():

    start_time = time.perf_counter()

    weather, attendance, assessments = await asyncio.gather(
        fake_weather_request(),
        fake_attendance_request(),
        fake_assessment_request()
    )

    end_time = time.perf_counter()

    return {
        "weather": weather,
        "attendance": attendance,
        "assessments": assessments,
        "duration": round(end_time - start_time, 2)
    }
import asyncio

import httpx
from fastapi import APIRouter, HTTPException, status

from app.routers.attendance import attendance_records
from app.routers.assessments import assessments


router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


async def get_weather_data():

    params = {
        "latitude": -27.95,
        "longitude": 153.40,
        "current": (
            "temperature_2m,"
            "apparent_temperature,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone": "auto"
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            OPEN_METEO_URL,
            params=params,
            timeout=10.0
        )

        response.raise_for_status()

    data = response.json()
    current = data["current"]

    return {
        "temperature": current["temperature_2m"],
        "apparent_temperature": current["apparent_temperature"],
        "weather_code": current["weather_code"],
        "wind_speed": current["wind_speed_10m"]
    }


async def get_attendance_summary():

    await asyncio.sleep(0)

    present = sum(
        1
        for record in attendance_records
        if record["status"] == "present"
    )

    absent = sum(
        1
        for record in attendance_records
        if record["status"] == "absent"
    )

    late = sum(
        1
        for record in attendance_records
        if record["status"] == "late"
    )

    return {
        "total_records": len(attendance_records),
        "present": present,
        "absent": absent,
        "late": late
    }


async def get_assessment_summary():

    await asyncio.sleep(0)

    return {
        "total_assessments": len(assessments),
        "assessments": [
            {
                "id": assessment["id"],
                "title": assessment["title"],
                "due_date": assessment["due_date"]
            }
            for assessment in assessments
        ]
    }


@router.get("/")
async def get_dashboard():

    try:

        weather, attendance, assessment_data = await asyncio.gather(
            get_weather_data(),
            get_attendance_summary(),
            get_assessment_summary()
        )

    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to retrieve dashboard weather data"
        )

    return {
        "weather": weather,
        "attendance": attendance,
        "assessments": assessment_data
    }
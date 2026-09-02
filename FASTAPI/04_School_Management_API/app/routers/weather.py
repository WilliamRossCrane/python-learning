import httpx

from fastapi import APIRouter, HTTPException, Query, status


router = APIRouter(
    prefix="/api/v1/weather",
    tags=["Weather"]
)


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


@router.get("/current")
async def get_current_weather(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180)
):

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "apparent_temperature,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone": "auto"
    }

    try:
        async with httpx.AsyncClient() as client:

            response = await client.get(
                OPEN_METEO_URL,
                params=params,
                timeout=10.0
            )

            response.raise_for_status()

    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to retrieve weather data"
        )

    data = response.json()

    current = data["current"]

    return {
        "location": {
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "timezone": data["timezone"]
        },
        "weather": {
            "temperature": current["temperature_2m"],
            "apparent_temperature": current["apparent_temperature"],
            "weather_code": current["weather_code"],
            "wind_speed": current["wind_speed_10m"]
        },
        "time": current["time"]
    }
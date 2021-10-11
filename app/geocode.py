from typing import Dict

from fastapi import APIRouter
from geopy.geocoders import Nominatim
import geopy

router = APIRouter()
locator = Nominatim(user_agent="DS API - Family Promise")


@router.post("/geocode/")
async def get_latitude_longitude(address_input: Dict):
    """
    Please post an address as a JSON object with this format:
{"address": "123 Gilman Dr W", "address_line2": "", "city": "Seattle", "state": "WA", "zip": "98119", "country": "United States"}

    The output will be a JSON object with the following format:
{"latitude": 47.64971, "longitude": -117.39764}
    """
    if not address_input:
        return {"latitude": 47.64971, "longitude": -117.39764}
    address_string = " ".join(val for val in address_input.values() if val)
    if type(locator.geocode(address_string)) == geopy.location.Location:
        return {
            "latitude": locator.geocode(address_string).latitude,
            "longitude": locator.geocode(address_string).longitude,
        }
    else:
        address_string = " ".join(
            val for key, val in address_input.items() if key != "address_line2")
        if type(locator.geocode(address_string)) == geopy.location.Location:
            return {
                "latitude": locator.geocode(address_string).latitude,
                "longitude": locator.geocode(address_string).longitude,
            }
        else:
            return {"Result": "Error, location not found"}

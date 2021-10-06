from fastapi import APIRouter
from geopy.geocoders import Nominatim
import geopy

router = APIRouter()


@router.post("/geocode/")
async def get_latitude_longitude(address_input: dict):
    """
    Please post an address as a JSON object with this format:

{"address": "123 Gilman Dr W", "address_line2": "", "city": "Seattle", "state": "WA", "zip": "98119", "country": "United States"}

    The output will be a JSON object with the following format:
{"latitude": 47.64971, "longitude": -117.39764}

    Default values point to a the Family Promise Homeless Shelter
    """
    lat_long = {"latitude": 47.649710, "longitude": -117.397640}
    locator = Nominatim(user_agent='DS API - Family Promise')
    address_string = " ".join(val for val in address_input.values() if val)
    if type(locator.geocode(address_string)) == geopy.location.Location:
        lat_long["latitude"] = locator.geocode(address_string).latitude
        lat_long["longitude"] = locator.geocode(address_string).longitude
    return lat_long

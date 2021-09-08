from fastapi import APIRouter, Request
from geopy.geocoders import Nominatim
import geopy

router = APIRouter()


@router.post("/geocode/")
async def get_latitude_longitude(request: Request):
    # request needs to be instantiated or you'll get a self error
    """
    Please post an address as a JSON object with this exact format:
    {
        "address": "123 Gilman Dr W",
        "address_line2": "",
        "city": "Seattle",
        "state": "WA",
        "zip": "98119",
        "country": "United States"
    }

    All values should be a string
    if there is no address_line2, the value should still be an empty string
    """
    # await because async...
    # request.json() retrieves the info that is being posted to this route
    address_input = await request.json()
    # instantiate latitude + longitude dict
    lat_long = {"latitude": 0, "longitude": 0}
    # instantiate geopy locator using user_agent from previous cohort
    locator = Nominatim(user_agent='DS API - Family Promise')
    # address string
    address_string = "".join(
        line + " "
        for line in address_input.values()
        if type(line) == str and line != ""
    )
    # ensure the provided address is properly recognized
    if type(locator.geocode(address_string)) == geopy.location.Location:
        # update latitude and longitude with real values
        lat_long["latitude"] = locator.geocode(address_string).latitude
        lat_long["longitude"] = locator.geocode(address_string).longitude
    else:
        # TODO - use better default values than "0" when an address is invalid or missing
        # possible ideas:
        # latitude and longitude of zip code if available
        # or
        # simply avoid mapping points if there are no valid coordinates
        # and have an additional section on the map visualization for unmapped services
        #
        # and if all else fails, and we still *need* numbers that aren't 0...
        # use "headquarters" or some other default point determined by stakeholder
        None

    return lat_long

from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/geocode/")
async def get_latitude_longitude(request: Request):
    # request needs to be instantiated or you'll get a self error
    """
    Provide address with this format:
    TODO - add address format
    """

    # await because async...
    # request.json() retrieves the info that is being posted to this route
    address_input = await request.json()

    lat_long = {"latitude": 0, "longitude": 0}

    # TODO - use a better default value than 0

    # TODO - update lat + long with real values
    return lat_long

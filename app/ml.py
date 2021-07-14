"""Machine learning functions"""
from fastapi import APIRouter


router = APIRouter()


@router.post("/recommendations/{query_json}")
async def run_model(query_json):
    """
    TODO: This function will run the recommendation model and return a JSON as
    a result.

    ### Parameters
    --------------
    query_json : JSON
        The query posted to the endpoint to be used as model input.
    TODO: Describe object format

    ### Returns
    -----------
    JSON
        A JSON of the result from the model
        TODO: Describe object format
    """
    pass

import json
from fastapi import APIRouter
from app.db import get_db
from datetime import datetime
router = APIRouter()
db = get_db()


@router.post("/eligibility/{id}")
async def check_eligibility(id: str) -> dict:
    """
    Checks for eligibility for services based on service provider data.

    ### Parameters
    --------------
    id
        A household_id entry from the households table.
    
    ### Returns
    -----------
    JSON
        "resident_assistance_eligibility": bool
        "reduced_bus_fare_eligiblity": bool
    """

    result = {}

    eligible_income = check_income(id)
    household_size = get_household_size(id) # Currently unused
    has_senior_citizen, has_veteran = check_recipients(id)

    # Check for resident assistance eligibility
    # This will change if more information is added to the database
    if eligible_income:
        result["resident_assistance_eligibility"] = True
    else:
        result["resident_assistance_eligibility"] = False

    # Check for reduced bus fare eligibility
    # This will change when we have information regarding qualifying
    # disabilities and/or SSI or Medicare cards
    if has_senior_citizen:
        result["reduced_bus_fare_eligiblity"] = True
    else:
        result["reduced_bus_fare_eligiblity"] = False

    return result


def get_household_size(id: str) -> int:
    """
    Gets the size of a household from its id.

    ### Parameters
    --------------
    id
        A household_id from the households table
    
    ### Returns
    -----------
    int
        The size of the household as the number of household members
    """
    size = db.execute(
        f"SELECT household_size FROM households WHERE household_id = {id}")
    return size.fetchall()[0][0]


def check_income(id):
    """
    Checks if family income is below the current $61,680 threshold.

    ### Parameters
    --------------
    id
        A household_id from the households table
    
    ### Returns
    -----------
    bool
        True if the household's income is at or below the threshold
    """
    query_string = f"""
    SELECT household_income
    FROM households
    WHERE household_id = {id}
    """
    # This should not be hard coded, and is currently a placeholder with the 
    # correct value as of 7/18/2021 for Spokane, WA.
    threshold = 61680
    income = db.execute(query_string).fetchall()[0][0]
    return True if income <= threshold else False


def check_recipients(id: str) -> 'tuple[bool]':
    """
    Checks whether or not recipients in a household are above the age of 65, and
    if they're a veteran.

    ### Parameters
    --------------
    id
        A household_id from the households table
    
    ### Returns
    -----------
    tuple[bool]
        A tuple containing two booleans, denoting if a family has members over
        the age of 65 and/or veterans, respectively.
    """
    query_string = f"""
    SELECT recipient_date_of_birth, recipient_veteran_status
    FROM recipients
    WHERE household_id = {id}
    """
    recipients = db.execute(query_string).fetchall()
    vet_status = False
    over_65 = False
    for person in recipients:
        age = (datetime.now().date() - person[0]).days / 365.25 # Accounts for leapyear
        if person[1] == True:
            vet_status = True
        if age >= 65:
            over_65 = True
    return over_65, vet_status

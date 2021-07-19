import json
from fastapi import APIRouter, Depends
from sqlalchemy.sql.expression import true
from app.db import get_db
from datetime import datetime

router = APIRouter()

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
    has_senior_citizen, has_veteran, has_disability, has_valid_ssi, \
        has_valid_medicare_card = check_recipients(id)

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


def check_household_stability(id: str, db = Depends(get_db)) -> bool:
    """
    Checks if a household has been flagged as unstable.

    ### Parameters
    --------------
    id
        A household_id from the households table

    ### Returns
    -----------
    bool
        True if household flagged as unstable, otherwise False
    """
    query_string = f"""
    SELECT is_unstable
    FROM households
    WHERE household_id = {id}
    """
    with db.begin():
        result = db.execute(query_string).fetchall()[0][0]
    return result


def get_household_size(id: str, db = Depends(get_db)) -> int:
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
    with db.begin():
        size = db.execute(
            f"SELECT household_size FROM households WHERE household_id = {id}")
    return size.fetchall()[0][0]


def check_income(id, db = Depends(get_db)):
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
    with db.begin():
        income = db.execute(query_string).fetchall()[0][0]
    return True if income <= threshold else False


def check_recipients(id: str, db = Depends(get_db)) -> 'tuple[bool]':
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
        A tuple containing the following, in order:
        over_65
        vet_status
        has_disability
        has_valid_ssi
        has_valid_medicare_card
    """
    query_string = f"""
    SELECT recipient_date_of_birth, recipient_veteran_status, has_disability,
    has_valid_ssi, has_valid_medicare_card
    FROM recipients
    WHERE household_id = {id}
    """
    with db.begin():
        recipients = db.execute(query_string).fetchall()
    vet_status = False
    over_65 = False
    has_disability = False
    has_valid_ssi = False
    has_valid_medicare_card = False
    for person in recipients:
        # There's a better way to do this line
        age = (datetime.now().date() - person[0]).days / 365.25 # Accounts for leapyear

        if age >= 65:
            over_65 = True
        if person[1]:
            vet_status = True
        if person[2]:
            has_disability = True
        if person[3]:
            has_valid_ssi = True
        if person[4]:
            has_valid_medicare_card = True
    return over_65, vet_status, has_disability, has_valid_ssi, \
        has_valid_medicare_card

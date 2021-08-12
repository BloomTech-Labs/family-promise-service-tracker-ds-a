from fastapi import APIRouter, Depends
import sqlalchemy
from datetime import datetime
from app.db import get_db
from typing import Tuple

router = APIRouter()


@router.post("/eligibility/{household_id}")
async def check_eligibility(household_id: str, db=Depends(get_db)) -> dict:
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
    # household_size and has_veteran are currently unused, but could prove
    # necessary at a later date, when more information about services
    # is available. An example of where this may come in handy is SNAP
    # (food stamp) eligibility.

    # May need to be changed depending on how the id is posted. Single quotes
    # necessary for queries.
    household_id = f"'{household_id}'"
    result = {}
    eligible_income = check_income(household_id, db)
    household_size = get_household_size(household_id, db)  # Currently unused
    has_senior_citizen, has_veteran, has_disability, has_valid_ssi, \
        has_valid_medicare_card = check_recipients(household_id, db)
    is_unstable = check_household_stability(household_id, db)

    # Check for resident assistance eligibility
    # This will change if more information is added to the database
    if eligible_income or is_unstable:
        result["resident_assistance_eligibility"] = True
    else:
        result["resident_assistance_eligibility"] = False

    # Check for reduced bus fare eligibility
    if has_senior_citizen \
            or has_disability \
            or has_valid_ssi \
            or has_valid_medicare_card:
        result["reduced_bus_fare_eligiblity"] = True
    else:
        result["reduced_bus_fare_eligiblity"] = False

    return result


def check_household_stability(
        household_id: str, db: sqlalchemy.engine.Connection) -> bool:
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
    WHERE household_id = {household_id}
    """
    with db.begin():
        result = db.execute(query_string).fetchall()[0][0]
    return result


def get_household_size(household_id: str, db: sqlalchemy.engine.Connection) -> int:
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
            f"SELECT household_size FROM households WHERE household_id = {household_id}")
    return size.fetchall()[0][0]


def check_income(household_id, db: sqlalchemy.engine.Connection):
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
    WHERE household_id = {household_id}
    """
    # This should not be hard coded
    # It is currently a placeholder with the
    # correct value as of 7/18/2021 for Spokane, WA.
    threshold = 61680

    with db.begin():
        income = db.execute(query_string).fetchall()[0][0]
    return True if income <= threshold else False


def check_recipients(household_id: str,
                     db: sqlalchemy.engine.Connection) -> Tuple[
                        bool, bool, bool, bool, bool]:
    """
    Checks whether or not recipients in a
    household are above the age of 65, and
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
    WHERE household_id = {household_id}
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
        age = (datetime.now().date() - person[0]).days / 365.25

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

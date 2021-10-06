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
        "reduced_bus_fare_eligibility": bool
    """
    household_id = f"'{household_id}'"
    income = check_income(household_id, db)
    stability = check_household_stability(household_id, db)
    bus_fare = any(check_recipients(household_id, db))
    return {
        "resident_assistance_eligibility": income or stability,
        "reduced_bus_fare_eligibility": bus_fare,
    }


def check_household_stability(household_id: str,
                              db: sqlalchemy.engine.Connection) -> bool:
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
    with db.begin():
        result = db.execute(f"""
        SELECT is_unstable
        FROM households
        WHERE household_id = {household_id}""").fetchall()[0][0]
    return result


def get_household_size(household_id: str,
                       db: sqlalchemy.engine.Connection) -> int:
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
        size = db.execute(f"""
        SELECT household_size 
        FROM households 
        WHERE household_id = {household_id}""").fetchall()[0][0]
    return size


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
    # This should not be hard coded
    # It is currently a placeholder with the
    # correct value as of 7/18/2021 for Spokane, WA.
    threshold = 61680 / 12

    with db.begin():
        income = db.execute(f"""
        SELECT household_monthly_income
        FROM households
        WHERE household_id = {household_id}""").fetchall()[0][0]
    return income <= threshold


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
    with db.begin():
        recipients = db.execute(f"""
        SELECT recipient_date_of_birth, recipient_veteran_status, has_disability,
        has_valid_ssi, has_valid_medicare_card
        FROM recipients
        WHERE household_id = {household_id}""").fetchall()
    is_senior = lambda age: (datetime.now().date() - age).days / 365.25 >= 65
    return (
        any(is_senior(row[0]) for row in recipients),
        any(row[1] for row in recipients),
        any(row[2] for row in recipients),
        any(row[3] for row in recipients),
        any(row[4] for row in recipients),
    )

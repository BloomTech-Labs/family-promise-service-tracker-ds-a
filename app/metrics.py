from fastapi import APIRouter, Depends
from app.db import get_db
from datetime import datetime
import pandas as pd
router = APIRouter()


@router.get("/total_served")
async def get_total_served(conn = Depends(get_db)) -> int:
    """
    Returns the total number of recipients
    TODO: Return recipients relavent to user

    ### Returns
    -----------
    int
        total_served
    """
    query_string = """
    SELECT COUNT(*)
    FROM recipients
    """
    with conn.begin():
        total_served = conn.execute(query_string).fetchall()[0][0]
    return total_served


@router.get("/families_served")
async def get_families_served(conn = Depends(get_db)) -> int:
    """
    Returns the total number of families
    TODO: Return only those relavent to the user
    ### Returns
    -----------
    int
        families_served
    """
    query_string = """
    SELECT COUNT(*)
    FROM households
    """
    with conn.begin():
        families_served = conn.execute(query_string).fetchall()[0][0]
    return families_served


@router.get("/children_served")
async def get_children_served(conn = Depends(get_db)) -> int:
    """
    Returns the number of recipients under 18, not inclusive.

    ### Returns
    -----------
    int
        children_served
    """
    query_string = """
    SELECT recipient_date_of_birth
    FROM recipients
    """
    with conn.begin():
        dates_of_birth = conn.execute(query_string).fetchall()

    df = pd.DataFrame(dates_of_birth)
    # Today
    now = datetime.now().date()
    # Subtract 18 years from today
    eighteen_years_ago = datetime(year = now.year - 18,
                                  month = now.month,
                                  day = now.day)
    #filter df by DoB's past eighteen years ago
    df = df[df[0] >= eighteen_years_ago.date()]
    # grab the count
    children_served = df.count()[0]
    return int(children_served)

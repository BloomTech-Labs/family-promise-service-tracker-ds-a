from fastapi import APIRouter, Depends
from app.db import get_db
from datetime import datetime
import pandas as pd

router = APIRouter()


@router.get("/total_served")
async def get_total_served(conn=Depends(get_db)) -> int:
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
async def get_families_served(conn=Depends(get_db)) -> int:
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
async def get_children_served(conn=Depends(get_db)) -> int:
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
    eighteen_years_ago = datetime(year=now.year - 18,
                                  month=now.month,
                                  day=now.day)
    # Filter df by DoB's past eighteen years ago
    df = df[df[0] >= eighteen_years_ago.date()]
    # Grab the count
    children_served = df.count()[0]
    return int(children_served)


@router.get("/genders_served")
async def get_genders_served(conn=Depends(get_db)) -> int:
    """
    Returns the count of each gender served.

    ### Returns
    -----------
    list
        genders_served
    """
    query_string = """
    SELECT genders.gender, (SELECT COUNT(*) 
    FROM recipients 
    WHERE recipients.gender_id = genders.gender_id) 
    AS TOTAL FROM genders
    """
    with conn.begin():
        genders = conn.execute(query_string).fetchall()
    return genders


@router.get("/races_served")
async def get_races_served(conn=Depends(get_db)) -> int:
    """
    Returns the count of each race served.

    ### Returns
    -----------
    list
        races_served
    """
    query_string = """
    SELECT races.race, (SELECT COUNT(*) 
    FROM recipients
    WHERE recipients.race_id = races.race_id) 
    AS TOTAL FROM races
    """
    with conn.begin():
        races = conn.execute(query_string).fetchall()
    return races


@router.get("/ethnicities_served")
async def get_ethnicities_served(conn=Depends(get_db)) -> int:
    """
    Returns the count of each ethnicity served.

    ### Returns
    -----------
    list
        ethnicities_served
    """
    query_string = """
    SELECT ethnicities.ethnicity, (SELECT COUNT(*) 
    FROM recipients
    WHERE recipients.ethnicity_id = ethnicities.ethnicity_id) 
    AS TOTAL FROM ethnicities
    """
    with conn.begin():
        ethnicities = conn.execute(query_string).fetchall()
    return ethnicities


@router.get("/program_enrollment")
async def get_program_enrollment(conn=Depends(get_db)) -> int:
    """
    Returns the count of services done for each program.

    ### Returns
    -----------
    list
        program_enrollment
    """
    query_string = """
    SELECT programs.program_name, (SELECT COUNT(*) 
    FROM service_entries, service_type_programs
    WHERE service_entries.service_type_program_id = service_type_programs.service_type_program_id 
    AND service_type_programs.program_id = programs.program_id) 
    AS TOTAL FROM programs
    """
    with conn.begin():
        programs = conn.execute(query_string).fetchall()
    return programs


@router.get("/services_given")
async def get_services_given(conn=Depends(get_db)) -> int:
    """
    Returns the count of each service provided.

    ### Returns
    -----------
    list
        services_given
    """
    query_string = """
    SELECT service_types.service_type_name, (SELECT COUNT(*) 
    FROM service_entries, service_type_programs
    WHERE service_entries.service_type_program_id = service_type_programs.service_type_program_id 
    AND service_type_programs.service_type_id = service_types.service_type_id) 
    AS TOTAL FROM service_types
    """
    with conn.begin():
        services = conn.execute(query_string).fetchall()
    return services


@router.get("/locations_of_service")
async def get_locations(conn=Depends(get_db)) -> int:
    """
    Returns the count of services at each type of location.

    ### Returns
    -----------
    list
        locations_of_service
    """
    query_string = """
    SELECT location_types.location_type, (SELECT COUNT(*) 
    FROM service_entries, locations
    WHERE service_entries.location_id = locations.location_id
    AND locations.location_type_id = location_types.location_type_id) 
    AS TOTAL FROM location_types
    """
    with conn.begin():
        locations = conn.execute(query_string).fetchall()
    return locations

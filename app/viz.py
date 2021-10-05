"""Data visualization functions"""

from fastapi import APIRouter
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from geopy.geocoders import Nominatim

router = APIRouter()


@router.post('/vizmap/{query_json}')
async def visual(query_json):
    """
    Creates an interactive map with dots pertaining to location of service.
    The dots on the map are color coded by service.
    Because there is no latitude or longitude in BE database, we geocode in order
    to get latitude and longitude.
    With the acquired latitude and longitude, the map visualization can be created
    and sent to the BE in JSON form.

    Input:
    -------
    query_json : JSON object
        Sent to DS API from BE

    Output:
    -------
    JSON object sent back to BE
    """
    # read in json from BE
    with open(query_json, 'r') as f:
        data_path_vet = json.loads(f.read())

    # create dataframe from loaded json
    df = pd.DataFrame.from_dict(data_path_vet)
    # instantiate locator
    locator = Nominatim(user_agent='DS API - Family Promise')
    # the columns that together make up the full address
    cols = ['address', 'address_line2', 'city', 'state', 'zip', 'country']
    # if address_line2 is null, it will be replaced by ""
    df['address_line2'] = df['address_line2'].apply(
        lambda x: "" if x is None else x)
    # put the parts of the address together into a single column
    # each part will be separated by comma, which is what geocode expects
    df['full_address'] = df[cols].apply(
        lambda row: ','.join(row.values.astype(str)), axis=1)
    # get latitude of each address
    df['latitude'] = df['full_address'].apply(
        lambda address: locator.geocode(address).latitude)
    # get longitude of each address
    df['longitude'] = df['full_address'].apply(
        lambda address: locator.geocode(address).longitude)

    fig = px.scatter_mapbox(df, lat="latitude", lon='longitude',
                            color="service_description",  # dots on map will be colored by service
                            # service name will be seen when hovering over dot
                            hover_name="service_description",
                            hover_data={
                                'service_description': False,
                                'latitude': False,
                                'longitude': False
                            },
                            zoom=11
                            )

    # make figure have desired layout
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(showlegend=False)
    fig.update_traces(marker=dict(size=6))  # larger dots
    # make figure a json that can then be rendered by FE
    return fig.to_json()


@router.post('/veteran_counts/{query_json}')
async def veteran_counts(query_json):
    """
    This function will return a bar chart of the count of veterans being
    served by Family Promise, in JSON form.
    """

    # read in json
    with open(query_json, 'r') as f:
        data_path_vet = json.loads(f.read())

    # create dataframe from loaded json
    df = pd.DataFrame.from_dict(data_path_vet)

    # get value counts of veterans vs non veterans
    veteran_count = df['recipient_veteran_status'].value_counts()
    # make bar chart of the counts
    veteran_counts_fig = px.bar(
        veteran_count,
        labels={'index': 'Veteran Status', 'value': 'Count'},
        title='Number of Veterans being Served'
    )
    # get rid of legend, because it does not have useful information (in this case)
    veteran_counts_fig.update_layout(showlegend=False)

    # make figure a json that can then be rendered by FE
    return veteran_counts_fig.to_json()


@router.post('/age_metric/{query_json}')
async def age_metric(query_json):
    """
    This function will return a table visual of the count of recipients by age group being
    served by Family Promise, in JSON form.
    """
    # read in json
    with open(query_json, 'r') as f:
        data_path_age = json.loads(f.read())
    # create dataframe from loaded json
    df = pd.DataFrame.from_dict(data_path_age)
    df = df.dropna()
    # configure dataset and calculate age based on date of birth from today
    df['DOB'] = pd.to_datetime(
        df['recipient_date_of_birth'], infer_datetime_format=False)
    now = pd.to_datetime('now')
    df_ages = df[['recipient_id', 'DOB']]
    df_ages['age'] = df_ages['DOB'].apply(lambda x: now - x).astype('<m8[Y]')

    # binning ages into groups
    bins = [0, 3, 6, 13, 18, 24, 40, 60, 125]
    labels = ['0-2 yrs', '3-6 yrs', '7-13 yrs', '14-18 yrs',
              '19-24 yrs', '25-40 yrs', '41-60 yrs', '61+ yrs', ]
    df_ages['Age_Bins'] = pd.cut(
        df_ages.age, bins, labels=labels, include_lowest=True, right=False)
    df_age_grouped = df_ages.groupby(['Age_Bins']).count()
    df_age_grouped = df_age_grouped.drop(columns=['age'])
    # make table of the counts
    fig_age_counts = go.Figure(data=[go.Table(header=dict(values=['Age', 'Count'], fill_color='paleturquoise',
                               align='center'), cells=dict(values=[df_age_grouped.index, df_age_grouped.recipient_id]))])
    # get rid of legend, because it does not have useful information (in this case)
    fig_age_counts.update_layout(showlegend=False)
    # make figure a json that can then be rendered by FE
    return fig_age_counts.to_json()

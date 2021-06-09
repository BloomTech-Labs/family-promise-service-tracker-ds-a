"""Data visualization functions"""

from fastapi import APIRouter
import pandas as pd
import plotly.express as px
import numpy as np

router = APIRouter()


@router.get('/vizmap')
async def visual():
    # load in dataset
    DATA_PATH = 'https://raw.githubusercontent.com/Lambda-School-Labs/family-promise-service-tracker-ds-a/main/data/services_by-zipcode.csv'
    df = pd.read_csv(DATA_PATH, index_col=0)

    fig = px.scatter_mapbox(df, lat="latitude", lon='longitude',
                            color="city",  # which column to use to set the color of markers
                            hover_name="zipcode",  # column added to hover information
                            size='counts',
                            zoom=4,
                            )

    fig.update_layout(mapbox_style="open-street-map")
    fig.show()

    return fig.to_json()


@router.post('/veteran_counts')
async def veteran_counts(be_json):
    """
    If JSON provided by BE is simple, this function will return a bar chart of the count 
    of veterans being served by Family Promise, in JSON form.

    If the desired figure is for veteran counts in a specific service, then this function
    would have to be altered.
    TODO: find out what the JSON's that the BE will send over look like
    """
    # read in json
    df = pd.read_json(be_json)
    # get value counts of veterans vs non veterans
    veteran_counts = df['recipient_veteran_status'].value_counts()
    # make bar chart of the counts
    veteran_counts_fig = px.bar(
        veteran_counts,
        labels={'index': 'Veteran Status', 'value': 'Count'},
        # title might have to be an f-string, especially when creating
        # this vislualization will be done by service or other filters
        title='Number of Veterans being Served by Family Promise'
    )
    # get rid of legend, because it does not have useful information (in this case)
    veteran_counts_fig.update_layout(showlegend=False)

    # make figure a json that can then be rendered by FE
    return veteran_counts_fig.to_json()

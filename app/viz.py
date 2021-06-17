"""Data visualization functions"""

from fastapi import APIRouter
import pandas as pd
import plotly.express as px
import json

router = APIRouter()


@router.get('/vizmap')
async def visual():
    # load in dataset
    DATA_PATH = './data/services_by-zipcode.csv'
    df = pd.read_csv(DATA_PATH)

    fig = px.scatter_mapbox(df, lat="latitude", lon='longitude',
                            color="city",  # which column to use to set the color of markers
                            hover_name="zipcode",  # column added to hover information
                            size='counts',
                            zoom=4,
                            )

    fig.update_layout(mapbox_style="open-street-map")
    fig.show()

    return fig.to_json()


@router.post('/veteran_counts/{query_json}')
async def veteran_counts(query_json):
    """
    This function will return a bar chart of the count of veterans being 
    served by Family Promise, in JSON form.
    """

    # read in json
    with open(query_json, 'r') as f:
        Data_path_vet = json.loads(f.read())

    # create dataframe from loaded json
    df = pd.DataFrame.from_dict(Data_path_vet)

    # get value counts of veterans vs non veterans
    veteran_counts = df['recipient_veteran_status'].value_counts()
    # make bar chart of the counts
    veteran_counts_fig = px.bar(
        veteran_counts,
        labels={'index': 'Veteran Status', 'value': 'Count'},
        title='Number of Veterans being Served'
    )
    # get rid of legend, because it does not have useful information (in this case)
    veteran_counts_fig.update_layout(showlegend=False)

    # make figure a json that can then be rendered by FE
    return veteran_counts_fig.to_json()

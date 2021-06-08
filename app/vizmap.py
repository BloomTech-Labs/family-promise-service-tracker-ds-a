"""Data visualization functions"""

from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

router = APIRouter()


@router.get('/vizmap')
async def visual():
    # load in dataset
    DATA_PATH = 'https://raw.githubusercontent.com/Lambda-School-Labs/family-promise-service-tracker-ds-a/main/data/services_by-zipcode.csv'
    df = pd.read_csv(DATA_PATH, index_col=0)

    fig = px.scatter_mapbox(df, lat="latitude", lon='longitude',
                     color="city", # which column to use to set the color of markers
                     hover_name="zipcode", # column added to hover information
                     size='counts',
                     zoom=4,
                     )

    fig.update_layout(mapbox_style="open-street-map")
    fig.show()
    
    return fig.to_json()

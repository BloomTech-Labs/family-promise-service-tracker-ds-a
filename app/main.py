from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import db, viz, eligibility, metrics, geocode


app = FastAPI(
    title='DS API - Family Promise',
    docs_url='/',
    version='0.39.6',
)

app.include_router(db.router, tags=['Database'])
app.include_router(viz.router, tags=['Visualizations'])
app.include_router(eligibility.router, tags=['Eligibility'])
app.include_router(metrics.router, tags=['Metrics'])
app.include_router(geocode.router, tags=['Geocode'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    """ To run this API locally use the following commands
    cd family-promise-service-tracker-ds-a
    python -m app.main
    """
    import uvicorn
    uvicorn.run(app)

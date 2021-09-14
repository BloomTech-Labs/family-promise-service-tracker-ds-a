from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import db, ml, viz, eligibility, metrics, geocode


description = """

To use these interactive docs:
- Click on an endpoint below
- Click the **Try it out** button
- Edit the Request body or any parameters
- Click the **Execute** button
- Scroll down to see the Server response Code & Details
"""

app = FastAPI(
    title='DS API - Family Promise',
    description=description,
    docs_url='/',
    version='0.38.02',
)

app.include_router(db.router, tags=['Database'])
app.include_router(ml.router, tags=['Machine Learning'])
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
    import uvicorn
    uvicorn.run(app)

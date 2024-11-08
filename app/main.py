from fastapi import FastAPI
from app.routers import label_analysis, test

app = FastAPI()
app.include_router(label_analysis.router)
app.include_router(test.router)

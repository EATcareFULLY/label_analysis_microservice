from fastapi import FastAPI
from app.routers import label_analysis

app = FastAPI()
app.include_router(label_analysis.router)

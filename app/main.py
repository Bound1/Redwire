from fastapi import FastAPI
from api.image_generation import router as image_router

app = FastAPI()

app.include_router(image_router, prefix="/api")


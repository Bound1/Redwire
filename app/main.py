from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.image_generation import router as image_router

app = FastAPI()

app.include_router(image_router, prefix="/api")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])

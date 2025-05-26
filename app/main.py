from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.add_file import router as add_new_file_router
from app.api.get_file_info import router as file_info_router
from app.db.database import init_db

app = FastAPI(
    lifespan=init_db
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(add_new_file_router)
app.include_router(file_info_router)

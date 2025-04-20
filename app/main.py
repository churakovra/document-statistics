from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.controllers.add_new_file_controller import add_new_file_router
from app.controllers.get_file_info_controller import get_file_info_router
from app.database import init_db

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
app.include_router(get_file_info_router)

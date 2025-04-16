from fastapi import FastAPI

from app.controllers.add_new_file_controller import add_new_file_router
from app.controllers.root_controller import root_router
from app.database import init_db

app = FastAPI(
    lifespan=init_db
)

app.include_router(root_router)
app.include_router(add_new_file_router)

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import routers
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

for router in routers:
    app.include_router(router)

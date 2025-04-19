from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.controllers.add_new_file_controller import add_new_file_router
from app.controllers.get_file_info_controller import get_file_info_router
from app.database import init_db

app = FastAPI(
    lifespan=init_db
)

app.include_router(add_new_file_router)
app.include_router(get_file_info_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

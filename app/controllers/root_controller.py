from fastapi import APIRouter

root_router = APIRouter()


@root_router.get("/")
async def root():
    return {"message": "Hi! I'm alive! If u're from Lesta games, u're welcome!"}

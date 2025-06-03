from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hi! I'm alive! If u're from Lesta games, u're welcome!"}

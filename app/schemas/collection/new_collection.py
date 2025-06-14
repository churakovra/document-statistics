from pydantic import BaseModel


class NewCollection(BaseModel):
    label: str
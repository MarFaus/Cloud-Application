from pydantic import BaseModel


class ServiceSchema(BaseModel):
    id: int
    name: str
    status: str

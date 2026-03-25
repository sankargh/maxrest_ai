from pydantic import BaseModel


class Location(BaseModel):
    location: str
    description: str
    siteid: str
    locationuid: int


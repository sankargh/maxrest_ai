from pydantic import BaseModel


class Asset(BaseModel):
    assetnum: str
    description: str
    location: str
    siteid: str
    assetuid: int




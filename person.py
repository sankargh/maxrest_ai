from pydantic import BaseModel

class Person(BaseModel):
    personid: int
    name: str
    age: int
    email: str
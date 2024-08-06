from pydantic import BaseModel, Field

class User(BaseModel):
    email: str = Field(default="admin@gmail.com")
    password: str = Field(default="admin")
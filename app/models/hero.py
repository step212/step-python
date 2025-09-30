from sqlmodel import Field, SQLModel
from typing import Union

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: Union[int, None] = Field(default=None, index=True)

class Hero(HeroBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    secret_name: str

class HeroPublic(HeroBase):
    id: int

class HeroCreate(HeroBase):
    secret_name: str

class HeroUpdate(SQLModel):
    name: Union[str, None] = None
    age: Union[int, None] = None
    secret_name: Union[str, None] = None
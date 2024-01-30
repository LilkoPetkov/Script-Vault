from typing import Union

from pydantic import BaseModel


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

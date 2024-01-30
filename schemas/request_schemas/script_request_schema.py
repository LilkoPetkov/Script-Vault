from typing import Union, Annotated

from fastapi import Query
from pydantic import BaseModel


class ScriptRequestSchema(BaseModel):
    name: Annotated[Union[str, None], Query(
        min_length=2,
        max_length=25,
        default="script name"
    )]

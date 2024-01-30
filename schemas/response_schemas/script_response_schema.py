from typing import Union, Annotated

from fastapi import Query
from pydantic import BaseModel


class ScriptResponseSchema(BaseModel):
    name: Annotated[Union[str, None], Query(
        min_length=2,
        max_length=25,
        default="script name"
    )]


class AdminScriptResponseSchema(ScriptResponseSchema):
    path: Union[str, None]
    script_id: Union[int, None]


class ScriptsMeResponseSchema(ScriptResponseSchema):
    script_id: Union[int, None]

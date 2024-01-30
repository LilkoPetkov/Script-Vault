from typing import Optional
from typing import Union, Annotated

from fastapi import Query
from pydantic import EmailStr

from schemas.base_schemas.user_base_schema import UserBase
from schemas.response_schemas.user_response_schema import UserMeResponseSchema


class UserRequestSchema(UserBase):
    username: Annotated[Union[str, None], Query(
        min_length=2,
        max_length=25,
        default="username"
    )]
    email: Annotated[Union[EmailStr, None], Query(
        min_length=3,
        max_length=255,
        default="email"
    )]
    hashed_password: Annotated[Union[str, None], Query(
        min_length=5,
        max_length=255,
        default="password",
        format="password"
    )]

    class Config:
        from_attributes = True


class UserUpdateRequestSchema(UserMeResponseSchema):
    hashed_password: Union[str, None] = None

    class Config:
        from_attributes = True


class UserUpdatePatchOptionalSchema(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None
    is_active: Optional[bool] = None

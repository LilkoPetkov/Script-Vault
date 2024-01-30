from typing import Union

from pydantic import EmailStr

from schemas.base_schemas.user_base_schema import UserBase
from schemas.response_schemas.token_response_schema import TokenResponseSchema


class UserResponseSchema(UserBase, TokenResponseSchema):
    access_token: Union[str, None] = None
    token_type: Union[str, None] = None

    class Config:
        from_attributes = True


class UserMeResponseSchema(UserBase):
    username: Union[str, None] = None
    email: Union[EmailStr, None] = None
    is_active: Union[bool, None] = None

    class Config:
        from_attributes = True


class AdminUserMeResponseSchema(UserMeResponseSchema):
    user_id: Union[int, None]


class UserAllResponseSchema(UserMeResponseSchema):
    user_id: Union[int, None] = None
    is_admin: Union[bool, None] = None
    email: Union[EmailStr, str] = str

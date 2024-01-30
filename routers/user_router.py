from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from crud_functions.user_crud import update_user_full

from fastapi.security import OAuth2PasswordRequestForm
from auth.user_auth import get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, authenticate_user, \
    user_is_admin
from schemas.request_schemas.user_request_schemas import UserRequestSchema, UserUpdateRequestSchema, \
    UserUpdatePatchOptionalSchema
from schemas.response_schemas.user_response_schema import UserResponseSchema, UserMeResponseSchema, \
    UserAllResponseSchema
from schemas.response_schemas.script_response_schema import AdminScriptResponseSchema
from database.db import get_db
from crud_functions.user_crud import user_exists_email, user_exists_username, add_user, update_user_info, delete_user, \
    read_users, find_user, read_users_scripts
from schemas.response_schemas.token_response_schema import TokenResponseSchema
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "not found"}}
)


# User details endpoint
@router.get("/me", response_model=UserMeResponseSchema)
async def read_users_me(
        current_user: Annotated[UserMeResponseSchema, Depends(get_current_active_user)]
):
    return current_user


# Get all users
@router.get("/all", response_model=List[UserAllResponseSchema])
async def all_users(
        user: Annotated[UserRequestSchema, Depends(user_is_admin)],
        db: Session = Depends(get_db)
) -> object:
    return read_users(db=db)


# Get specific user
@router.get("/user/{user_id}", response_model=UserMeResponseSchema)
async def search_user(
        user_id: int,
        user: Annotated[UserRequestSchema, Depends(user_is_admin)],
        db: Session = Depends(get_db),
) -> object:
    return find_user(db=db, user_id=user_id)


# Read user scripts
@router.get("/{user_id}/scripts", response_model=List[AdminScriptResponseSchema])
async def read_user_scripts(
        user_id: int,
        user: Annotated[UserRequestSchema, Depends(user_is_admin)],
        db: Session = Depends(get_db),
) -> object:
    return read_users_scripts(db=db, user_id=user_id)


# Register endpoint
@router.post("/register", response_model=UserResponseSchema, status_code=201)
async def register_user(
        user: UserRequestSchema,
        db: Session = Depends(get_db),
) -> object:
    if user_exists_email(db=db, email=user.email):
        raise HTTPException(status_code=400, detail="email already in use")
    if user_exists_username(db=db, username=user.username):
        raise HTTPException(status_code=400, detail="username already in use")

    user = add_user(db=db, user_details=user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Login
@router.post("/login", response_model=TokenResponseSchema)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Update - Patch
@router.patch("/update", status_code=200, response_model=UserMeResponseSchema)
async def update_user_details(
        user: Annotated[UserRequestSchema, Depends(get_current_active_user)],
        user_details: UserUpdatePatchOptionalSchema,
        db: Session = Depends(get_db)
) -> object:
    return update_user_info(db=db, user=user, user_data=user_details)


# Update - Put
@router.put("/update", status_code=200, response_model=UserMeResponseSchema)
async def update_user(
        user: Annotated[UserRequestSchema, Depends(get_current_active_user)],
        user_details: UserUpdateRequestSchema,
        db: Session = Depends(get_db)
) -> object:
    return update_user_full(db=db, user_data=user_details, user=user)


# Delete
@router.delete("/delete/{user_id}", status_code=200)
async def remove_user(
        user_id: int,
        user: Annotated[UserRequestSchema, Depends(user_is_admin)],
        db: Session = Depends(get_db)
) -> dict:
    return delete_user(db=db, user_id=user_id)

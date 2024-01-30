from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from auth.user_auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from database.db import get_db
from schemas.response_schemas.token_response_schema import TokenResponseSchema

router = APIRouter(
    responses={404: {"description": "Not found"}},
    tags=["Addons"]
)


@router.post("/token", response_model=TokenResponseSchema)
async def login_for_access_token(
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

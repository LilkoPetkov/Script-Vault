from datetime import datetime, timedelta
from typing import Union

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from database.db import get_db
from models.user_model import User
from schemas.response_schemas.token_response_schema import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user


# Tokenisation

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

# Create hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Create token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Get the user
async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
) -> object:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="inactive user")

    return current_user


async def user_is_admin(
        current_user: Annotated[User, Depends(get_current_active_user)]
) -> object:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="user does not have the needed authorisation")

    return current_user

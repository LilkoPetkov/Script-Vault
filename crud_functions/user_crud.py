from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from auth.user_auth import get_password_hash
from database.db import get_db
from models.script_model import Script
from models.user_model import User
from schemas.request_schemas.user_request_schemas import UserRequestSchema, UserUpdatePatchOptionalSchema


# Get all users
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> object:
    users = db.query(User).offset(skip).limit(limit).all()

    return users


# Add user
def add_user(db: Session, user_details: UserRequestSchema) -> object:
    user = User(
        username=user_details.username,
        email=user_details.email,
        hashed_password=get_password_hash(user_details.hashed_password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    script_one = db.query(Script).filter(Script.name == "search_replace.py").first()
    script_two = db.query(Script).filter(Script.name == "import_db.py").first()

    user.scripts.append(script_one)
    user.scripts.append(script_two)

    db.add_all([user, script_one, script_two])
    db.commit()

    return user


# Update user - PUT
def update_user_full(db: Session, user_data: UserRequestSchema, user: User) -> object:
    updated_user = db.query(User).filter(User.user_id == user.user_id)

    if not updated_user:
        raise HTTPException(
            status_code=400,
            detail="user does not exist",
            headers={"X-Error": "Invalid/Missing User"}
        )
    if user_exists_email(db=db, email=user_data.email):
        raise HTTPException(
            status_code=400,
            detail="email already exists",
            headers={"X-Error": "Invalid/Missing Email"}
        )

    user_data.hashed_password = get_password_hash(user_data.hashed_password)

    updated_user.update(user_data.model_dump(), synchronize_session=False)
    db.commit()

    return user


# User update - PATCH
def update_user_info(db: Session, user_data: UserUpdatePatchOptionalSchema, user: User) -> object:
    if user_exists_email(db=db, email=user_data.email):
        raise HTTPException(
            status_code=400,
            detail="email already exists",
            headers={"X-Error": "Invalid/Missing Email"}
        )
    if user_exists_username(db=db, username=user_data.username):
        raise HTTPException(
            status_code=400,
            detail="username already exists",
            headers={"X-Error": "Invalid/Missing Email"}
        )

    updated_user = db.query(User).filter(User.user_id == user.user_id).first()

    if user_data.hashed_password:
        user_data.hashed_password = get_password_hash(user_data.hashed_password)

    data = user_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(updated_user, key, value)

    db.add(updated_user)
    db.commit()
    db.refresh(updated_user)

    return user


def user_exists_email(db: Session, email: str) -> object:
    return db.query(User).filter(User.email == email).first()


def user_exists_username(db: Session, username: str) -> object:
    return db.query(User).filter(User.username == username).first()


# Delete user
def delete_user(db: Session, user_id: int) -> dict:
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="user does not exist",
            headers={"X-Error": "Invalid/Missing User"}
        )

    db.delete(user)
    db.commit()

    return {"message": f"user with ID: {user_id} has been deleted"}


# Get specific user
def find_user(db: Session, user_id: int) -> dict:
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="user does not exist",
            headers={"X-Error": "Invalid/Missing User"}
        )

    return user


# Show specific user's scripts - Admin
def read_users_scripts(db: Session, user_id: int) -> object:
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="user does not exist",
            headers={"X-Error": "Invalid/Missing User"}
        )

    return user.scripts

import os
import shutil

from fastapi import HTTPException, Depends, File
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from addons.script_paths import find_script_folder, get_script
from database.db import get_db
from models.script_model import Script
from models.user_model import User


# Add scripts
def add_script(
        db: Session,
        file: File,
) -> object:
    check_script = db.query(Script).filter(file.filename == Script.name).first()

    if check_script:
        raise HTTPException(
            status_code=400,
            detail="script name already exists",
            headers={"X-Error": "Invalid Script Name"}
        )

    script_folder = find_script_folder()

    script = Script(
        name=file.filename,
        path=script_folder
    )

    # Add script file
    new_file = os.path.join(script_folder, file.filename)

    with open(new_file, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

        # Commit script in db
    db.add(script)
    db.commit()
    db.refresh(script)

    return script


# See all scripts
def read_scripts(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> object:
    scripts = db.query(Script).offset(skip).limit(limit).all()

    return scripts


# Delete script
def delete_script(db: Session, script_id: int) -> dict:
    script = db.query(Script).filter(Script.script_id == script_id).first()

    if not script:
        raise HTTPException(
            status_code=400,
            detail="script does not exist",
            headers={"X-Error": "Invalid/Missing Script"}
        )

    # Remove from db
    db.delete(script)
    db.commit()

    # Remove file
    found_script = get_script(script.name)
    try:
        os.remove(found_script)
    except FileNotFoundError as _:
        raise HTTPException(
            status_code=400,
            detail=f"script does not exist",
            headers={"X-Error": "Invalid/Missing Script"}
        )

    return {"message": f"script: '{script.name}' has been deleted"}


# Update path
def path_update(db: Session, new_path: str = find_script_folder()) -> dict:
    scripts = db.query(Script)
    print(scripts)
    scripts.update({"path": new_path}, synchronize_session=False)
    db.commit()

    return read_scripts(db=db)


# Assign script to user
def assing_script(db: Session, user_id: int, script_id: int) -> object:
    user = db.query(User).filter(User.user_id == user_id).first()
    script = db.query(Script).filter(Script.script_id == script_id).first()

    if user and script and not script_exists(db=db, user_id=user_id, script_id=script_id):
        user.scripts.append(script)

        db.add_all([user, script])
        db.commit()

        return {"message": f"script: {script.name} assigned to user: {user.username}"}

    else:
        raise HTTPException(
            status_code=400,
            detail="invalid script/user",
            headers={"X-Error": "Invalid/Missing Script/User"}
        )


def script_exists(db: Session, user_id: int, script_id: int) -> bool:
    query = text(f"select * from user_scripts where s_id = {script_id} and u_id = {user_id};")
    script = list(db.execute(query))

    if script:
        return True
    return False


# Get user scripts
def user_scripts(current_user: User) -> dict:
    return current_user.scripts


# Search for specific script
def search_specific_script(db: Session, script_id: int) -> object:
    script = db.query(Script).filter(Script.script_id == script_id).first()

    if script:
        return script

    raise HTTPException(
        status_code=400,
        detail="invalid/missing script",
        headers={"X-Error": "Invalid/Missing Script"}
    )


# Return scripts
def find_script_crud(db: Session, script_id: int, user_id) -> object:
    if script_exists(db=db, script_id=script_id, user_id=user_id):
        script = db.query(Script).filter(Script.script_id == script_id).first()
        full_path = os.path.join(script.path, script.name)

        return full_path

    raise HTTPException(
        status_code=400,
        detail="invalid/missing script",
        headers={"X-Error": "Invalid/Missing Script"}
    )


# Remove script from user without deleting the script file - Admin
def remove_script_from_user_crud(db: Session, script_id: int, user_id: int) -> object:
    if script_exists(db=db, script_id=script_id, user_id=user_id):
        query = text(f"delete from user_scripts where u_id={user_id} and s_id={script_id};")
        db.execute(query)
        db.commit()

        return {"message": f"Script ID: {script_id} has been removed from user ID: {user_id}"}

    raise HTTPException(
        status_code=400,
        detail="invalid/missing script",
        headers={"X-Error": "Invalid/Missing Script"}
    )

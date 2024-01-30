from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    # relation
    scripts = relationship(
        "Script",
        secondary="user_scripts",
        back_populates="users"
    )


user_scripts = Table(
    "user_scripts", Base.metadata,
    Column("s_id", ForeignKey("scripts.script_id"), primary_key=True),
    Column("u_id", ForeignKey("users.user_id"), primary_key=True)
)

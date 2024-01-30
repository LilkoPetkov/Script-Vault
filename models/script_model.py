from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.db import Base


class Script(Base):
    __tablename__ = "scripts"

    script_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    path = Column(String, index=True)

    # relation
    users = relationship(
        "User",
        secondary="user_scripts",
        back_populates="scripts"
    )

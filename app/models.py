from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.mysql import CHAR
import uuid
from .database import Base

class User(Base):
    __tablename__ = "users"
    uuid = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    fullname = Column(String(64), nullable=False)
    studylevel = Column(String(32), nullable=False)
    age = Column(Integer, nullable=False)

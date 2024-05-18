from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Books(Base):
    __tablename__ = "Books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    rating = Column(Integer)

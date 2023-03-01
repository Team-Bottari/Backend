from sqlalchemy import Column, TEXT, INT, BIGINT, BOOLEAN, DATE, DATETIME
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Member(Base):
    __tablename__ = "member"

    member_id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    id = Column(TEXT, nullable=False)
    pw = Column(TEXT, nullable=False)
    nick_name = Column(TEXT, nullable=False)
    name = Column(TEXT, nullable=False)
    phone = Column(TEXT, nullable=False)
    birth = Column(DATE, nullable=False)
    credit_rating = Column(INT, nullable=False)
    profile_picture = Column(TEXT, nullable=True)
    status = Column(BOOLEAN, nullable=False)
    create_at = Column(DATETIME, nullable=False,  default=datetime.datetime.utcnow)
    last_login = Column(DATETIME, nullable=True)
    last_logout = Column(DATETIME, nullable=True)

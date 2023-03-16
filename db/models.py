from sqlalchemy import Column, TEXT, INT, BIGINT, BOOLEAN, DATE, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqladmin import ModelView
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
    withdrawal = Column(BOOLEAN, nullable=False)
    create_at = Column(DATETIME, nullable=False,  default=datetime.datetime.utcnow)
    last_login = Column(DATETIME, nullable=True)
    last_logout = Column(DATETIME, nullable=True)
    certificate_num = Column(TEXT, nullable=False)
    certificate_status = Column(BOOLEAN, nullable=False)

        
class Member_Admin(ModelView,model=Member):
    column_list = [ eval(f"Member.{column.name}") for column in Member().__table__.columns]
    page_size = 50
    page_size_options = [25, 50, 100, 200]
if __name__=="__main__":
    pass

    
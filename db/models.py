from sqlalchemy import Column, TEXT, INT, BIGINT, BOOLEAN, DATE, DATETIME,ForeignKey,JSON
from sqlalchemy.ext.declarative import declarative_base
from sqladmin import ModelView
import datetime

Base = declarative_base()

class Member(Base):
    __tablename__ = "member"
    member_id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True, unique=True)
    email = Column(TEXT, nullable=False)
    pw = Column(TEXT, nullable=False)
    nick_name = Column(TEXT, nullable=False)
    name = Column(TEXT, nullable=False)
    phone = Column(TEXT, nullable=False)
    birth = Column(DATE, nullable=False)
    credit_rating = Column(INT, nullable=False)
    profile_picture = Column(TEXT, nullable=True)
    withdrawal = Column(BOOLEAN, nullable=False)
    create_at = Column(DATETIME, nullable=False,  default=datetime.datetime.utcnow)
    update_at = Column(DATETIME, nullable=False,  default=datetime.datetime.utcnow)
    last_login = Column(DATETIME, nullable=True)
    last_logout = Column(DATETIME, nullable=True)
    certificate_num = Column(TEXT, nullable=False)
    certificate_status = Column(BOOLEAN, nullable=False)

        
class Member_Admin(ModelView,model=Member):
    column_list = [ eval(f"Member.{column.name}") for column in Member().__table__.columns]
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    
class Posting(Base):
    __tablename__ = "posting"
    posting_id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True, unique=True)
    title = Column(TEXT, nullable=False)
    content = Column(TEXT, nullable=False)
    price = Column(BIGINT, nullable=False)
    sold_out = Column(BOOLEAN, nullable=False)
    member_id = Column(BIGINT, ForeignKey('member.member_id'),nullable=False)
    create_at = Column(DATETIME, nullable=False,  default=datetime.datetime.utcnow)
    image_path = Column(JSON,nullable=True)
    views = Column(BIGINT, nullable=False)
    like = Column(BIGINT, nullable=False)
    update_nums = Column(BIGINT, nullable=False)
    update_at = Column(DATETIME, nullable=False,  default=datetime.datetime.utcnow)
    category = Column(TEXT, nullable=False)
    remove = Column(BOOLEAN, nullable=False)
    can_discount = Column(BOOLEAN, nullable=False,)
    average_price = Column(BIGINT, nullable=True)
    lowest_price = Column(BIGINT, nullable=True)
    
class Posting_Admin(ModelView,model=Posting):
    column_list = [ eval(f"Posting.{column.name}") for column in Posting().__table__.columns]
    page_size = 50
    page_size_options = [25, 50, 100, 200]

if __name__=="__main__":
    pass

    
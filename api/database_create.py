from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    'mysql+pymysql://root:duddnjsgl912!@iyoungman-skuniv-mysql-1.chxhgtrfuigt.ap-northeast-2.rds.amazonaws.com/blog_crawling?charset=utf8',
    convert_unicode=True, echo=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(engine)

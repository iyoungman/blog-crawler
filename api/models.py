from sqlalchemy import Column, Integer, String
from api.database import Base


class Info(Base):
    __tablename__ = 'infos'
    id = Column(Integer, primary_key=True)
    email = Column(String(50))
    blog = Column(String(100))
    blog_type = Column(String(50))

    def __init__(self, email=None, blog=None, blog_type=None):
        self.email = email
        self.blog = blog
        self.blog_type = blog_type

    def __repr__(self):
        return "<Info(name='%s', email='%s', blog_type='%s)>" % (self.email, self.blog, self.blog_type)

    @property
    def get_email(self):
        return self.email

    @property
    def get_blog(self):
        return self.blog

    @property
    def get_blog_type(self):
        return self.blog_type

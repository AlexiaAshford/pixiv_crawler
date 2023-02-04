from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class ImageDB(Base):
    __tablename__ = 'images'
    id = Column(String, primary_key=True)
    image_title = Column(String)
    image_caption = Column(String)
    image_author = Column(String)
    image_author_id = Column(String)
    image_tags = Column(String)
    image_url = Column(String)
    image_page_count = Column(Integer)
    image_create_date = Column(String)
    cover = Column(String)

    def __repr__(self):
        return "<Image(id='%s', title='%s')>" % (self.id, self.image_title)


class UserDB(Base):
    __tablename__ = 'users_info'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from config import Config


engine = create_engine(Config.DATABASE_URI)
db_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class ItemList(Base):
    __tablename__ = 'ItemList'

    id = Column(Integer, primary_key=True, autoincrement=True)
    list_name = Column(String, index=True, unique=True)
    items = relationship('Item', backref='list_items', lazy=True)
    created_by = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return self.attributes()

    def __str__(self):
        return str(self.attributes())

    def attributes(self):
        return {key: value for key, value in self.__dict__.items() if key[0] != '_'}


class Item(Base):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_list = Column(String, ForeignKey(ItemList.list_name))
    item_name = Column(String, index=True, unique=True)
    created_by = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return self.attributes()

    def __str__(self):
        return str(self.attributes())

    def attributes(self):
        return {key: value for key, value in self.__dict__.items() if key[0] != '_'}
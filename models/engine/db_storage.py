#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """This class manages storage of hbnb models in a SQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates a new storage object"""
        self.__engine = create_engine('mysql+mysqldb://hbnb_dev:hbnb_dev_pwd@localhost/hbnb_dev_db', pool_pre_ping=True)

    def all(self, cls=None):
        """Query all objects for the current session"""
        if cls:
            return {obj.to_dict()['__class__'] + '.' + obj.id: obj for obj in self.__session.query(cls).all()}
        else:
            obj_dict = {}
            for cls_name in Base.__subclasses__():
                for obj in self.__session.query(cls_name).all():
                    obj_dict[obj.to_dict()['__class__'] + '.' + obj.id] = obj
            return obj_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload the session and database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the current session"""
        self.__session.remove()

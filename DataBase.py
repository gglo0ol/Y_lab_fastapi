from pydantic import BaseModel, UUID4
from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker

from uuid import uuid4


DATABASE_URL = "postgresql://postgres:y_lab@localhost:5432/"        # Нужно использовать какое то другое имя БД
Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_uuid():
    return str(uuid4())


class Menu(Base):
    __tablename__ = "menus"
    id = Column(String, primary_key=True, default=get_uuid, unique=True)
    title = Column(String)
    description = Column(String)
    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete-orphan")

class Submenu(Base):
    __tablename__ = 'submenus'
    id = Column(String, primary_key=True, default=get_uuid, unique=True)
    menu_id = Column(String, ForeignKey("menus.id"))
    title = Column(String)
    description = Column(String)
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")

class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(String, primary_key=True, default=get_uuid, unique=True)
    title = Column(String)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(String, ForeignKey("submenus.id"))

    submenu = relationship("Submenu", back_populates="dishes")




Base.metadata.create_all(bind=engine)

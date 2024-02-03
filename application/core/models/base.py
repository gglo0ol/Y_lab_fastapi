from core.db import Base, get_uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(String, primary_key=True, default=get_uuid, unique=True)
    title = Column(String)
    description = Column(String)
    submenus = relationship(
        'Submenu', back_populates='menu', cascade='all, delete-orphan'
    )


class Submenu(Base):
    __tablename__ = 'submenus'
    id = Column(String, primary_key=True, default=get_uuid, unique=True)
    menu_id = Column(String, ForeignKey('menus.id'))
    title = Column(String)
    description = Column(String)
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship(
        'Dish', back_populates='submenu', cascade='all, delete-orphan'
    )


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(String, primary_key=True, default=get_uuid, unique=True)
    submenu_id = Column(String, ForeignKey('submenus.id'))
    title = Column(String)
    description = Column(String)
    price = Column(String)

    submenu = relationship('Submenu', back_populates='dishes')

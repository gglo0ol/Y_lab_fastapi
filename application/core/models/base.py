from application.core.db import Base
from sqlalchemy import Column, ForeignKey, String, UUID
from sqlalchemy.orm import relationship
from uuid import uuid4


class Menu(Base):
    __tablename__ = "menus"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    title = Column(String)
    description = Column(String)
    submenus = relationship(
        "Submenu", back_populates="menu", cascade="all, delete-orphan"
    )


class Submenu(Base):
    __tablename__ = "submenus"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    menu_id = Column(UUID, ForeignKey("menus.id"))
    title = Column(String)
    description = Column(String)
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship(
        "Dish", back_populates="submenu", cascade="all, delete-orphan"
    )


class Dish(Base):
    __tablename__ = "dishes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    submenu_id = Column(UUID, ForeignKey("submenus.id"))
    title = Column(String)
    description = Column(String)
    price = Column(String)

    submenu = relationship("Submenu", back_populates="dishes")

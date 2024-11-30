"""
This file has all the models for image manager
"""
from datetime import datetime
from typing import Any

from helpers import upload_file_to_s3
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base: Any = declarative_base()  # type: ignore


class User(Base):
    """
    Model to store user info
    """

    __tablename__ = "users"

    email = Column(String, primary_key=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    albums = relationship("Album", back_populates="owner")
    images = relationship("Image", back_populates="owner")


class Image(Base):
    """
    Model to store image info
    """

    __tablename__ = "images"

    id = Column(Integer, primary_key=True, nullable=False)
    owner = Column(String, ForeignKey("users.email"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    original_url = Column(String, nullable=False)
    downsampled_url = Column(String, nullable=True)
    date_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_updated = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True
    )

    owner = relationship("User", back_populates="images")
    albums = relationship("ImageAlbum", back_populates="image")

    def __init__(self, title, owner, description=None, file=None, **kwargs):
        super().__init__(title=title, owner=owner, description=description, **kwargs)

        if file:
            file_name = f"{self.title.replace(' ', '_').lower()}_{self.id}.jpg"
            s3_url = upload_file_to_s3(file, file_name)
            self.original_url = s3_url

    def save(self, session):
        session.add(self)
        session.commit()


class Album(Base):
    """
    Model to store album info
    """

    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, nullable=False)
    owner = Column(String, ForeignKey("users.email"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    date_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_updated = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True
    )

    owner = relationship("User", back_populates="albums")
    images = relationship("ImageAlbum", back_populates="album")


class ImageAlbum(Base):
    """
    Model to store mapping of image and an album
    """

    __tablename__ = "image_album"

    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)

    image = relationship("Image", back_populates="albums")
    album = relationship("Album", back_populates="images")

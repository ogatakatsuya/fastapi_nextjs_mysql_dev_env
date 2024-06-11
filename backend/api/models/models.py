from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    nickname = Column(String(20), nullable=True)
    biography = Column(String(1024), nullable=True)
    birth_day = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now, server_default=func.now(), nullable=False)
    
    posts = relationship("Post", back_populates="user")
    password = relationship("Password", back_populates="user", uselist=False)
    likes = relationship("Like", back_populates="user")
    
class Password(Base):
    __tablename__ = "passwords"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(1024), nullable=False)
    
    user_id = Column(Integer, ForeignKey('users.id', name="user_password"), nullable=False)
    user = relationship("User", back_populates="password")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(200))
    parent_id = Column(Integer, nullable=True, default=None)
    created_at = Column(DateTime, default=datetime.now(), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), server_default=func.now(), onupdate=datetime.now(), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id', name="fk_posts_users"), nullable=False)
    user = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post")

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', name="fk_likes_users"), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', name="fk_likes_posts"), nullable=False)
    
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='uix_user_post'),
    )

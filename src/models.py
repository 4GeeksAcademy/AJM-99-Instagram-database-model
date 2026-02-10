from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

user_follows = Table(
    "user_follows",
    db.metadata,
    Column("follower", ForeignKey("user.id")),
    Column("follow", ForeignKey("user.id"))
)



class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    latname: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")
    follow: Mapped[list["User"]] = relationship(secondary="user_follows", back_populates="followed_by")
    followed_by: Mapped[list["User"]] = relationship(secondary="user_follows", back_populates="follow")


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
            # do not serialize the password, its a security breach
        }   

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    media: Mapped[list["Media"]] = relationship(back_populates="posted_in")
    comments: Mapped[list["Comment"]] = relationship(back_populates="commented_in")
    author: Mapped["User"] = relationship(back_populates="posts")

    def serialize(self):
        return {
            "id": self.id,
            "media": (media.serialize() for media in self.media),
            "comments": (comment.serialize() for comment in self.comments),
            "author": self.author.serialize()
        } 


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    type: Mapped[int] = mapped_column(ForeignKey("mediatype.id"))
    url: Mapped[str] = mapped_column(unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    posted_in: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "posted_in_post": self.post_id
        } 
    

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    comment_text: Mapped[str] = mapped_column(String(120), nullable=False)
    author_id: Mapped[int] = relationship(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    commented_in: Mapped["Post"] = relationship(back_populates="comments")
    

    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment_text,
            "url": self.url,
            "posted_in_post": self.post_id,
            "author": self.author.serialize()
        } 

class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True, nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True, nullable=False)

class Mediatype(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    media_type: Mapped[str] = mapped_column(String(20), nullable=False)


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


post_coments = Table(
    "post_comments",
    db.metadata,
    Column("post_id", ForeignKey("post.id")),
    Column("comment", ForeignKey("comment.id"))
)

post_media = Table(
    "post_media",
    db.metadata,
    Column("post_id", ForeignKey("post.id")),
    Column("media", ForeignKey("media.id"))
)

user_posts = Table(
    "user_posts",
    db.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("post_id", ForeignKey("post.id"))
)

user_comments = Table(
    "user_comments",
    db.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("comment_id", ForeignKey("comment.id"))
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    latname: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    posts: Mapped[list["Post"]] = relationship(secondary="user_posts",back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(secondary="user_comments", back_populates="commented")


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
    media: Mapped[list["Media"]] = relationship(back_populates="content_in_post", secondary="post_media")
    comments: Mapped[list["Comment"]] = relationship(secondary="post_comments", back_populates="comments_in_post")
    author: Mapped["User"] = relationship(back_populates="posts", secondary="user_posts")


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[int] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(120), nullable=False)
    author_id: Mapped["User"] = relationship(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))



  
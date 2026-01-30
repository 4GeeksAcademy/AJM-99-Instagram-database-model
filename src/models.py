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

user_follows = Table(
    "user_follows",
    db.metadata,
    Column("user_id", ForeignKey("user.id"))
)

user_followers = Table(
    "user_followers",
    db.metadata,
    Column("user_id", ForeignKey("user.id"))
)


same_type_media = Table(
    "same_type_posts",
    db.metadata,
    Column("media_id", ForeignKey("media.id")),
    Column("type_id", ForeignKey("mediatype.id"))

)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    latname: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    posts: Mapped[list["Post"]] = relationship(secondary="user_posts",back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(secondary="user_comments", back_populates="commented")
    follows: Mapped[list["User"]] = relationship(secondary="user_follows", back_populates="follows")
    followers: Mapped[list["User"]] = relationship(secondary="user_followers", back_populates="followers")


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
    author: Mapped["User"] = relationship(back_populates="commented")
    

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
    media_same_type: Mapped[list["Media"]] = relationship(secondary="same_type_media", back_populates="media_of_type")


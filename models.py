from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

post_tag_association = db.Table(
    'post_tag_association',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    def __repr__(self):
        """Show info about user."""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.String,
                          nullable=False)
    
class Post(db.Model):
    def __repr__(self):
        """Show info about user."""
        u = self
        return f"<Post {u.id} {u.title} {u.content} {u.created_at} {u.user_id}>"
    
    __tablename__ = "post"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User')

    tags = db.relationship('Tag', secondary=post_tag_association, back_populates='posts')

class PostTag(db.Model):
    def __repr__(self):
        u = self
        return f"<PostTag {u.post_id} {u.tag_id}>"
    
    __tablename__= "post_tag"

    post_id = db.Column(db.Integer,
                       db.ForeignKey("post.id"),
                       primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tag.id"),
                       primary_key=True)
    
    
class Tag(db.Model):
    def __repr__(self):
        u = self
        return f"<Tag {u.id} {u.name}>"
    
    __tablename__ = "tag"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50),
                           nullable=False)
    
    posts = db.relationship('Post', secondary=post_tag_association, back_populates='tags')
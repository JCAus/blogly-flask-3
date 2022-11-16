"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

DEFAULT_IMG = "https://img.myloview.com/stickers/default-avatar-profile-icon-vector-social-media-user-image-700-240336019.jpg"

class User(db.Model):
    '''User class'''

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    auto_increment=True)

    first_name = db.Column(db.String(50),
                            nullable=False)
    
    last_name = db.Column(db.String(50),
                            nullable=False)

    img_url = db.Column(db.String(1000), default=DEFAULT_IMG)

    posts = db.relationship('Post', backref='users')

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name}"


class Post(db.Model):
    '''Posts class'''
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    auto_increment=True)
    
    title = db.Column(db.String(100), nullable=False)
                        

    content = db.Column(db.String(1000), nullable=False)
                        

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)

    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), 
                        primary_key=True, nullable=False)

    
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )
    
    
    


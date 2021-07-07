"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model): # usually only run this once after deployment otherwise you'll constantly be recreating data
    """User."""
    __tablename__ = "users"

    def __repr__(self):
        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}>"

    id = db.Column(db.Integer, # int not the same as SQL Integer, the ORM translates etween python and postgreSQL
                    primary_key=True,
                    autoincrement=True)
    
    first_name = db.Column(db.String(50),
                            nullable=False)

    last_name = db.Column(db.String(50)) #maybe null as default?

    image_url = db.Column(db.String(5000),
                            default='https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/200px-Question_mark_%28black%29.svg.png')
                            #maybe add a default image

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")           
    # https://stackoverflow.com/questions/5033547/sqlalchemy-cascade-delete 

class Post(db.Model):
    """Post."""  
    __tablename__ = "posts"

    def __repr__(self):
        return f"<Post id={self.id} title={self.title} content={self.content} created_at={self.created_at} user_id={self.user_id}>"

    id = db.Column(db.Integer, # int not the same as SQL Integer, the ORM translates etween python and postgreSQL
                    primary_key=True,
                    autoincrement=True)

    title = db.Column(db.String(50),
                        nullable=False)
    
    content = db.Column(db.String(5000),
                        nullable=False)

    created_at = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.datetime.now)  

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)                      

    
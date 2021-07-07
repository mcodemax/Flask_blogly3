"""Seed file for Users"""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add Users
user1 = User(first_name='Fname1', last_name="Lname1", image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Two_red_dice_01.svg/1200px-Two_red_dice_01.svg.png')
user2 = User(first_name='Fname2', last_name="Lname2")
user3 = User(first_name='Fname3', last_name="Lname3", image_url='https://i.ytimg.com/vi/MPV2METPeJU/maxresdefault.jpg')
user4 = User(first_name='Onlyhasfirstname')

# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)

# Commit--otherwise, this never gets saved!
db.session.commit()

postuser1_1 = Post(title='This A Title', content='This my content', user_id=1)
postuser1_2 = Post(title='This A Title2', content='This my content2', user_id=1)
postuser1_3 = Post(title='This A Title3', content='This my content2', user_id=1)
postuser1_4 = Post(title='This A Title4', content='This my content2', user_id=1)

db.session.add(postuser1_1)
db.session.add(postuser1_2)
db.session.add(postuser1_3)
db.session.add(postuser1_4)

db.session.commit()
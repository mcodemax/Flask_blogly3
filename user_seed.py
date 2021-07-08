"""Seed file for Users"""

from models import User, Post, Tag, PostTag, db
from app import app

def add_relation_tag(rel_to_append, tag_lst):
    
    for tag in tag_lst:
        rel_to_append.tags.append(tag)

    db.session.commit()


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

postuser1_1 = Post(title='Someone stole my money!', content='I got mugged', user_id=1)
postuser1_2 = Post(title='This A Title2', content='This my content2', user_id=1)
postuser1_3 = Post(title='This A Title3', content='This my content2', user_id=1)
postuser1_4 = Post(title='This A Title4', content='This my content2', user_id=1)
postuser2_1 = Post(title='LOL Funny Pics', content='Pretend this is funny.', user_id=2)
postuser2_2 = Post(title='This is a sad', content='Look at this bird crying', user_id=2)
postuser2_3 = Post(title='This A Educational and Smart', content='This is econ outlook for 2024: idk', user_id=2)

db.session.add(postuser1_1)
db.session.add(postuser1_2)
db.session.add(postuser1_3)
db.session.add(postuser1_4)
db.session.add(postuser2_1)
db.session.add(postuser2_2)
db.session.add(postuser2_3)

db.session.commit()

#adding in tags here

tag1 = Tag(name='sad')
tag2 = Tag(name='mad')
tag3 = Tag(name='econ')
tag4 = Tag(name='funny')
tag5 = Tag(name='education')
tag6 = Tag(name='misc')



db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)
db.session.add(tag4)
db.session.add(tag5)
db.session.add(tag6)

db.session.commit()

add_relation_tag(postuser1_2,
    [tag1, tag2, tag3, tag4, tag5, tag6])

add_relation_tag(postuser1_1,
    [tag1, tag2]) #you can create tags and make relations to them even
    #  before commiting tags; then adding relations to them if you so wish

add_relation_tag(postuser2_1, [tag4])

add_relation_tag(postuser2_2, [tag1])

add_relation_tag(postuser2_3, [tag5, tag3])
from unittest import TestCase
from app import app
from flask import session

from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:myPassword@localhost:5433/blogly_test' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False #prints in ipython the queries being run

#look at forex test cases, anmd

db.drop_all()
db.create_all()

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    # tests each route in app.py
    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        
        db.drop_all()
        db.create_all()

        User.query.delete()
        Post.query.delete()

    def tearDown(self):
        """Clean up"""
        db.session.rollback()

    def test_root_redirect(self):
        """Test root redirect"""
        with self.client as client: #ver of server that we can use in testing
            res = client.get('/') # sends the request

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/users")
    
    def test_userlist_html_rendering(self):
        """Test html rendering of the userlist"""
        user = User(first_name='Fname1', last_name="Lname1", image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Two_red_dice_01.svg/1200px-Two_red_dice_01.svg.png')
        db.session.add(user)
        db.session.commit()

        with self.client as client: 
            res = client.get('/', follow_redirects=True)
            html = res.get_data(as_text=True) 

            self.assertEqual(res.status_code, 200)
            self.assertIn('Fname1', html)

    def test_user_deletion(self):
        """Test if user info deleted"""
        user = User(first_name='Fname1', last_name="Lname1", image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Two_red_dice_01.svg/1200px-Two_red_dice_01.svg.png')
        db.session.add(user)
        db.session.commit()

        with self.client as client: 
            res = client.post('/users/1/delete', follow_redirects=True)
                   
            self.assertIsNone(User.query.get(1))

    def test_edit_render(self):
        """Test if user edit page renders; makeuser.html"""
        user = User(first_name='Fname1', last_name="Lname1", image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Two_red_dice_01.svg/1200px-Two_red_dice_01.svg.png')
        db.session.add(user)
        db.session.commit()
    
        with self.client as client: #ver of server that we can use in testing
            res = client.get('/users/1/edit') # sends the request
            html = res.get_data(as_text=True) 

            self.assertIn('edit-user', html)

    def test_post_deletion(self):
        """Test if post gets deleted"""
        user = User(first_name='Fname1', last_name="Lname1", image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Two_red_dice_01.svg/1200px-Two_red_dice_01.svg.png')
        db.session.add(user)
        db.session.commit()

        post = Post(title='This A Title', content='This my content', user_id=1)
        db.session.add(post)
        db.session.commit()

        with self.client as client: 
            res = client.post('/posts/1/delete', follow_redirects=True)
            html = res.get_data(as_text=True) 

            self.assertIsNone(Post.query.get(1))


    def test_post_edit_form_route(self):
        """Test if html form to edit a post is rendered"""
        user = User(first_name='Fname1', last_name="Lname1", image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Two_red_dice_01.svg/1200px-Two_red_dice_01.svg.png')
        db.session.add(user)
        db.session.commit()

        post = Post(title='This A Title', content='This my content', user_id=1)
        db.session.add(post)
        db.session.commit()
    
        with self.client as client: 
            res = client.get('/posts/1/edit', follow_redirects=True)
            html = res.get_data(as_text=True) 

            self.assertIn('This A Title',html)
            self.assertIn('Fname1',html)

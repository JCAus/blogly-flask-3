from unittest import TestCase

from app import app
from models import db, User, Post, PostTag, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewTestCase(TestCase):
    '''Test for views for users'''

    def setUp(self):
        """Add sample user"""
        User.query.delete()

        user = User(first_name="Jonny", last_name="Test", img_url="https://m.media-amazon.com/images/M/MV5BMTYxMDA1OTA2Nl5BMl5BanBnXkFtZTcwNTkzNzY4Mw@@._V1_.jpg")
        db.session.add(user)
        db.session.commit()

        post = Post(title="Hello World", content="This is my first post")
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        '''Clean up any fouled transactions'''

        db.session.rollback()

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jonny', html)
            self.assertIn('Test', html)


    def test_show_profile(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jonny', html)


    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Bobby", "last_name": "Testjr", "img_url": "https://www.tn.gov/content/dam/tn/twra/images/mammals/eastern-grey-squirrel/eastern-grey-squirrel_750x500.jpg"}
            resp = client.post('/add_user', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Bobby", html)

    def test_show_edit_profile(self):
        with app.test_client() as client:
            resp = client.get(f"/edit_profile/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit profile', html)

    def test_edit_profile(self):
        with app.test_client() as client:
            d = {"first_name": "Robby", "last_name": "Testsr", "img_url": "https://www.tn.gov/content/dam/tn/twra/images/mammals/eastern-grey-squirrel/eastern-grey-squirrel_750x500.jpg"}
            resp = client.post(f"/edit_profile/{self.user_id}", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Robby', html)

    def test_make_post(self):
        with app.test_client() as client:
            d = {"title": "test", "content": "foo"}
            resp = client.post(f'/post-page/{self.user_id}', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("foo", html)
            self.assertIn("test", html)

    def show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Hello World', html)
            self.assertIn('This is my first post', html)

    def test_edit_post(self):
        with app.test_client() as client:
            d = {"title": "Test2", "content": "testingtesting"}
            resp = client.post(f"/edit_post/{self.post_id}", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test2', html)

    
            
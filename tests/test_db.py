import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

#In-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        #Bind model classess to test db. Since we have a complete list of
        #all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)
    
    def tearDown(self):
        #Not strictly necessary since SQLite in-memory databases only live
        #for the duration of the connection, and in the next step we close
        #the connection...but a goot practice all the same.
        test_db.drop_tables(MODELS)

        #Close connection to db.
        test_db.close()
    
    def test_timeline_post(self):
        #Create two timeline posts.
        
        first_post = TimelinePost.create(name='John Doe',
        email='john@example.com', content='Hello world, I\'m John!')
        assert first_post.id == 1

        second_post = TimelinePost.create(name='Jane Doe',
        email='jane@example.com', content='Hello world, I\'m Jane!')
        assert second_post.id == 2

        #TODO: get timeline posts and assert that they are correct
        assert first_post == TimelinePost.get_by_id(1)
        assert second_post == TimelinePost.get_by_id(2)
import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title> Mario </title>" in html
        assert "we are kayla & mario" in html
        assert "home-button-kayla" in html
        assert "home-button-mario" in html
        #TODO add more tests relating to the home page
    
    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        
        #TODO Add more tests relating to the /api/timeline_post GET and POST apis
        self.client.post("/api/timeline_post", data={
            'name':'Charlie',
            'email':'charlie@net.com',
            'content':'Good luck Charlie'})
        
        response = self.client.get("/api/timeline_post")
        json = response.get_json()
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "Charlie"
        assert json["timeline_posts"][0]["email"] == "charlie@net.com"
        assert json["timeline_posts"][0]["content"] == "Good luck Charlie"
        
        #TODO Add more tests relating to the timeline page
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title> Timeline </title>" in html
        assert "timeline-form" in html
        assert "Name:</label>" in html
        assert "Email:</label>" in html
        assert "Content:</label>" in html
        assert "Send Post Request</button>" in html
        assert "timeline-posts" in html
    
    def test_malformed_timeline_post(self):
        #POST request missing name
        response = self.client.post("/api/timeline_post", data=
        {"email":"john@example.com", "content":"Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        #POST request with empty content
        response = self.client.post("/api/timeline_post", data=
        {"name":"John Doe", "email":"john@example.com", "content":""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        #POST request with malformed email
        response = self.client.post("/api/timeline_post", data=
        {"name":"John Doe", "email":"not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
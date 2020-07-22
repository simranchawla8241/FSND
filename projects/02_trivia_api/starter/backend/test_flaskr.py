import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question={
            "answer": "Agra",
            "category": 4,
            "difficulty": 1,
            "question": "Where is Taj Mahal located?"
        }       
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def get_paginated_questions(self):
        res=self.client.get('/questions')
        data=json.loads(res.data)

        self.assertEquals(res.status_code,200)
        self.assertEquals(data['success'],True)
        self.assertEquals(data['total_questions'],True)
        self.assertTrue(len(data['questions']))

    def test_404_request_beyond_valida_page(self):
        res=self.client.get('/questions?page=1000',json={'rating':1})
        data=json.loads(res.data)

        self.assertEquals(res.status_code,404)
        self.assertEquals(data['success'],False)
        self.assertEquals(data['message'],'resource not found')
    
    def test_delete_book(self):
        res=self.client.delete('/questions/1')
        data=json.loads(res.data)
        self.assertEquals(res.status_code,200)
        self.assertEquals(data['success'],True)
        self.assertEquals(data['deleted'],1)
        self.assertEquals(data['total_questions'],True)
        self.assertTrue(len(data['questions']))
    
    def test_422_if_question_does_not_exist(self):
        res=self.client.delete('/questions/1000')
        data=json.loads(res.data)

        self.assertEquals(res.status_code,422)
        self.assertEquals(data['success'],False)
        self.assertEquals(data['message'],'unprocessable')


    def create_new_question(self):
        res=self.client.post('/questions',json=self.new_question)
        data=json.loads(res.data)

        self.assertEquals(res.status_code,200)
        self.assertEquals(data['success'],False)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))

    def test_405_if_question_create_not_allowed(self):
        res=self.client.post('/questions/45',json=self.new_question)
        data=json.loads(res.data)

        self.assertEquals(res.status_code,405)
        self.assertEquals(data['success'],False)
        self.assertEquals(data['message'],'method not allowed')





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
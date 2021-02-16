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
        self.database_path = "postgres+psycopg2://postgres:postgres@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories_with_results(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_questions_with_results(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_get_questions_without_results(self):
        res = self.client().get('/questions/?page=10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    def test_store_question_success(self):
        newQuestion = {
            "question": 'New Question',
            "answer": 'New Answer',
            "category_id": 1,
            "difficulty": 5
        }
        res = self.client().post('/questions', json=newQuestion)
        data = json.loads(res.data)

        last_question_id = len(Question.query.all()) + 1
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(
            data['message'],
            'A New Question Has Been Added Successfully')
        self.assertTrue(data['question'], last_question_id)

    def test_store_question_error(self):
        newQuestion = {
            "question": 'New Question',
        }
        res = self.client().post('/questions', json=newQuestion)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable Entity')

    def test_delete_question_success(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(
            data['message'],
            'question has been deleted successfully')
        self.assertEqual(data['question_id'], 2)

    def test_delete_question_error(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    def test_get_cateogory_questions_with_results(self):
        res = self.client().get('/categories/1/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'], True)

    def test_get_cateogory_questions_without_results(self):
        res = self.client().get('/categories/1000/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    def test_quiz_success(self):
        info = {
            "quiz_category": {"id": 1, "type": "clicked"},
            "previous_questions": {}
        }
        res = self.client().post('/quiz', json=info)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_search_question_success(self):
        search = {
            "searchTerm": 'On ',
        }
        res = self.client().post('/questions/search', json=search)
        data = json.loads(res.data)

        questions = Question.query.filter(
            Question.question.ilike('%On %')).all()
        formattedQuestions = [question.format() for question in questions]
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['questions'], formattedQuestions)
        self.assertEqual(data['total_questions'], len(questions))

    def test_search_question_error(self):
        search = {
            "searchTerm": 'tesing tesing testing ',
        }
        res = self.client().post('/questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

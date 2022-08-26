from ast import JoinedStr
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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'nkirukka', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'How old is Barack Obama?',
            'answer': 56,
            'difficulty': 2,
            'category': 4
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO DONE
    Write at least one test for each test for successful operation and for expected errors.
    """

    """ GET ALL QUESTIONS """
    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 18)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])

    def test_404_no_question_found(self):
        res = self.client().get('/questions/19/p',  json={'difficulty': 10})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    """ DELETE """
    def test_delete_a_question(self):
        res = self.client().delete('/questions/18')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 18).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 18)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)

    def test_404_delete_question_id_not_found(self):
        res = self.client().delete('/questions/1999/q')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_422_delete_cannot_process(self):
        res =self.client().delete('/questions/57999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request cannot be processed')

    """ CREATE """
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['total_questions'])

    def test_405_not_allowed_add_new_question(self):
        res = self.client().post('/questions/89', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Operation not allowed')

    """ SEARCH """
    def test_get_question_search_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'old' })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
        self.assertTrue(data['total_questions'])

    def test_get_question_search_zero_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'zzzz' })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertFalse(data['total_questions'])

    """ CATEGORY """
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_non_existent_category(self):
        res = self.client().get('/categories/earth')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])

    def test_404_get_questions_beyond_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    """ QUIZZES"""
    def test_get_quiz(self):
        quiz = {'previous_questions': [],
                'quiz_category':{
                'id': '1', 'type': 'Science'}
                }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], '1')

    def test_422_cannot_process_get_quiz(self):
        quiz = {
            'previous_questions': []
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request cannot be processed')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
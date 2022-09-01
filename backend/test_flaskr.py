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
        self.database_path =  "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)
        
        self.new_question = {"question": "What's the 13th letter of the alphabet", "answer": "M", "category": 3, "difficulty": 5}

        self.new_quiz = {
            "previous_questions": [13, 14, 15], 
            "quiz_category": {'id': 3, 'type': 'Geography'}
            }
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        client_response = self.client().get("/categories")
        client_response_data = json.loads(client_response.data)

        success_data = client_response_data.get('success')
        categories_data = client_response_data.get('categories')
        total_categories_data = client_response_data.get('total_categories')

        self.assertEqual(client_response.status_code, 200)
        self.assertEqual(success_data, True)
        self.assertTrue(categories_data)
        self.assertTrue(total_categories_data)



    def test_404_sent_requesting_invalid_categories(self):
        client_response  = self.client().get("/categories/questions")

        client_response_data = json.loads(client_response.data)

        success_data = client_response_data.get('success')
        message_data = client_response_data.get('message')

        self.assertEqual(client_response.status_code, 404)
        self.assertEqual(success_data, False)
        self.assertEqual(message_data, "resource not found")



    def test_get_questions(self):
        client_response = self.client().get("/questions")
        client_response_data = json.loads(client_response.data)

        success_data = client_response_data.get('success')
        questions_data = client_response_data.get('questions')
        categories_data = client_response_data.get('categories')
        total_questions_data = client_response_data.get('total_questions')
        current_category_data = client_response_data.get('current_category')

        self.assertEqual(client_response.status_code, 200)
        self.assertEqual(success_data, True)
        self.assertTrue(questions_data)
        self.assertTrue(total_questions_data)
        self.assertTrue(categories_data)
        self.assertEqual(current_category_data, 'Null')



    def test_422_sent_requesting_non_existing_questions_page(self):
        client_response  = self.client().get("/questions?page=1000")
        client_response_data = json.loads(client_response.data)

        success_data = client_response_data.get('success')
        message_data = client_response_data.get('message')

        self.assertEqual(client_response.status_code, 422)
        self.assertEqual(success_data, False)
        self.assertEqual(message_data, "unprocessable")



    # def test_delete_question(self):
    #     client_response  = self.client().delete('/questions/17')
    #     client_response_data = json.loads(client_response.data)

    #     success_data = client_response_data.get('success')
    #     deleted_question_data = client_response_data.get('deleted_question')

    #     specific_question = Question.query.filter(Question.id == 17).one_or_none()

    #     self.assertEqual(client_response.status_code, 200)
    #     self.assertEqual(success_data, True)
    #     self.assertEqual(deleted_question_data, 17)
    #     self.assertEqual(specific_question, None)


    def test_404_if_question_does_not_exist(self):
        client_response = self.client().delete("/questions/1000")
        client_response_data = json.loads(client_response.data)
    
        success_data = client_response_data.get('success')
        message_data = client_response_data.get('message')

        self.assertEqual(client_response.status_code, 404)
        self.assertEqual(success_data, False)
        self.assertEqual(message_data, "resource not found")


    def test_create_new_question(self):
        client_response = self.client().post("/questions", json=self.new_question)
        client_response_data = json.loads(client_response.data)
        
        success_data = client_response_data.get('success')

        self.assertEqual(client_response.status_code, 200)
        self.assertEqual(success_data, True)


    def test_400_if_question_creation_fails(self):
        client_response = self.client().post("/questions")
        client_response_data = json.loads(client_response.data)
        
        success_data = client_response_data.get('success')
        message_data = client_response_data.get('message')

        self.assertEqual(client_response.status_code, 400)
        self.assertEqual(success_data, False)
        self.assertEqual(message_data, "bad request")

    def test_404_for_question_creation_wrong_endpoint(self):
        client_response = self.client().post("/questions/create", json=self.new_question)
        client_response_data = json.loads(client_response.data)
        
        success_data = client_response_data.get('success')
        message_data = client_response_data.get('message')

        self.assertEqual(client_response.status_code, 404)
        self.assertEqual(success_data, False)
        self.assertEqual(message_data, "resource not found")



    def test_search_questions(self):
        client_response = self.client().post('/questions/search', json={'searchTerm': 'title'})
        client_response_data = json.loads(client_response.data)

        success_data = client_response_data.get('success')
        questions_data = client_response_data.get('questions')
        total_questions_data = client_response_data.get('total_questions')
        current_category_data = client_response_data.get('current_category')
        
        self.assertEqual(client_response.status_code, 200)
        self.assertEqual(success_data, True)
        self.assertTrue(questions_data)
        self.assertTrue(total_questions_data)
        self.assertEqual(current_category_data, 'Null')
        


    def test_search_questions_wrong_method_error(self):
        client_response = self.client().get('/questions/search', json={})
        client_response_data = json.loads(client_response.data)
        
        success_data = client_response_data.get('success')
        message_data = client_response_data.get('message')

        self.assertEqual(client_response.status_code, 405)
        self.assertEqual(success_data, False)
        self.assertEqual(message_data, "method not allowed")


    def test_404_search_questions_wrong_endpoint_error(self):
        client_response = self.client().get('/questions/search/all', json={})
        client_response_data = json.loads(client_response.data)
        
        success_data = client_response_data.get('success')
        message_data = client_response_data.get('message')

        self.assertEqual(client_response.status_code, 404)
        self.assertEqual(success_data, False)
        self.assertEqual(message_data, "resource not found")
       
    
    def test_get_questions_by_category(self):
        client_response = self.client().get('/categories/1/questions')
        client_response_data = json.loads(client_response.data)

        success_data = client_response_data.get('success')
        questions_data = client_response_data.get('questions')
        total_questions_data = client_response_data.get('total_questions')
        current_category_data = client_response_data.get('current_category')
        
        self.assertEqual(client_response.status_code, 200)
        self.assertEqual(success_data, True)
        self.assertTrue(questions_data)
        self.assertTrue(total_questions_data)
        self.assertTrue(current_category_data)
    

    def test_404_question_by_category_error(self):
        client_response = self.client().get('/categories/1000/questions')
        client_response_data = json.loads(client_response.data)
        
        success_data = client_response_data.get('success')
        message_data = client_response_data.get('message')

        self.assertEqual(client_response.status_code, 404)
        self.assertEqual(success_data, False)
        self.assertEqual(message_data, "resource not found")
        


    def test_quiz_question(self):
        client_response = self.client().post('/quizzes', json=self.new_quiz)
        client_response_data = json.loads(client_response.data)

        questions_data = client_response_data.get('question')
    
        self.assertEqual(client_response.status_code, 200)
        self.assertTrue(questions_data)



    def test_422_quiz_question_error(self):
        client_response  = self.client().post('/quizzes', json={})
        client_response_data = json.loads(client_response.data)

        success_data = client_response_data.get('success')
        message_data = client_response_data.get('message')

        self.assertEqual(client_response.status_code, 422)
        self.assertEqual(success_data, False)
        self.assertEqual(message_data, "unprocessable")
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
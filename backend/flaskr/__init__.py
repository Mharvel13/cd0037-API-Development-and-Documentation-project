
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import random

from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10

def pagination_function(request, selection):

    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    data_formating = [data.format() for data in selection]
    paginated_data_formating = data_formating[start:end]

    return paginated_data_formating
 

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

   
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    # CORS(app, resource={r"*/api/" : {origins : "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,PATCH,POST,DELETE,OPTIONS"
        )
        return response
    

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            # select categories
            selected_categories = Category.query.order_by(Category.id).all()
            # format categories
            formatted_categories = {category.id:category.type for category in selected_categories} 
            
            if len(selected_categories) == 0:
                abort(404)
        
            return jsonify({
                'success': True,
                'categories':formatted_categories,
                'total_categories':len(selected_categories)     
            })

        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            # select questions and categories
            selected_questions = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()

            # paginate and format questions
            paginated_questions = pagination_function(request, selected_questions)
            
            # format categories
            formatted_categories = {category.id : category.type for category in categories} 

            # if questions is none, throw error
            if len(paginated_questions) == 0:
                abort(404)
            
            return jsonify({
                'success': True,
                'questions' : paginated_questions,
                'total_questions':len(selected_questions),
                'categories':formatted_categories,
                'current_category' : 'Null'
            })
        
        except:
            abort(422)

  
            
       
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            # get specific question by id
            specific_question = Question.query.get(question_id)

            # throw error if question does not exisit
            if specific_question is None:
                abort(404)
            
            # delete the question
            specific_question.delete()

            return jsonify(
                {
                    "success": True,
                    "deleted_question": question_id,
                }
            )
        except:
            abort(404)


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=["POST"])
    def create_question():
        # get json data from frontend
        new_question_data = request.get_json()

        # access the individual properties of the json data
        new_question = new_question_data.get('question', None)
        new_answer = new_question_data.get('answer', None)
        new_category = new_question_data.get('category', None)
        new_difficulty = new_question_data.get('difficulty', None)
        
        try:
            # insert into the database
            new_question_insert = Question(
                question=new_question,
                answer=new_answer, 
                difficulty=new_difficulty, 
                category=new_category
            )
            new_question_insert.insert()

            return jsonify({
                'success' : True,
            })

        except:
            abort(400)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def search_questions():

        try:
            # get the search term data
            search_data = request.get_json()
            search_term = search_data.get('searchTerm', None)

            # get questions that match with the search term
            search_questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            paginated_search_questions = pagination_function(request, search_questions)

            return jsonify({
                "success": True,
                'questions': paginated_search_questions,
                'total_questions': len(search_questions),
                'current_category': "Null",
            })

        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            # select the specific category
            specific_category = Category.query.get(category_id)

            # filter questions by category
            questions_by_category = Question.query.filter(Question.category == specific_category.id).all()

            # paginate the filtered questions
            paginated_questions_by_category = pagination_function(request, questions_by_category)

            return jsonify({
                "success": True,
                'questions': paginated_questions_by_category,
                'total_questions': len(questions_by_category),
                'current_category': specific_category.type
            })
        except:
            abort(404)


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def quiz_game():
        try:
            # get quiz  json data
            quiz_request = request.get_json()
            previous = quiz_request.get('previous_questions', None)
            category_data = quiz_request.get('quiz_category', None)
            
            # get questions based on the category choosen
            if category_data['id']:
                quiz_questions = Question.query.filter(
                    Question.category == category_data['id']).all()
            else:
                # get all the questions
                quiz_questions = Question.query.all()
            
            # format the quiz questions
            formatted_questions = [question.format() for question in quiz_questions]

            quiz_question_array = []

            for question in formatted_questions:
                if question['id'] not in previous:
                    quiz_question_array.append(question)

            if len(quiz_question_array) == 0:
                return jsonify({
                    'success': True
                })
            else:
                random_quiz_question = random.choice(quiz_question_array)

            return jsonify({
                'question': random_quiz_question
            })

        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400, 
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                "success": False, 
                "error": 404, 
                "message": "resource not found"
            }), 404
    

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success':False,
            'error':405,
            'message':'method not allowed'
        }), 405
        

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422, 
            "message": "unprocessable"
        }), 422
    
    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 500, 
            "message": "internal server error"
        }), 500
    

    return app


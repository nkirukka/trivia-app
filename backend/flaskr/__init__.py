import os
from unicodedata import category
from xml.dom.pulldom import ErrorHandler
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [q.format() for q in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    @TODO: DONE. Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    # CORS(app, resources={r"*/api/*" : {"origins": '*'}})
    """
    @TODO: DONE. Use the after_request decorator to set Access-Control-Allow
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
    @TODO DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        category = Category.query.order_by(Category.type.asc()).all()
        return jsonify({
            'success': True,
            'categories': [c.type for c in category]
        })

    """
    @TODO DONE:
    Create an endpoint to handle GET requests for questions
    """
    @app.route('/questions')
    def get_questions():
        all_quest = Question.query.order_by(Question.question).all()
        current_questions = paginate_questions(request, all_quest)

        if len(all_quest) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(all_quest),
            'categories': [cat.type for cat in Category.query.all()],
            'current_cateogry': []
        })

    """
    @TODO DONE:
    Create an endpoint to DELETE question using a question ID.
    """
    @app.route('/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):

        question = Question.query.filter(Question.id == q_id).one_or_none()
        try:
            if question is None:
                abort(404)
            else:
                question.delete()

                selection = Question.query.order_by(Question.question).all()
                current_questions = paginate_questions(request, selection)
                return jsonify({
                    'success': True,
                    'deleted': q_id,
                    'total_questions': len(selection),
                    'questions': current_questions
                })
        except:
            abort(422)

    """
    @TODO DONE:
    Create an endpoint to POST a new question,
    """
    """
    @TODO DONE:
    Create a POST endpoint to get questions based on a search term.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        search = body.get('searchTerm', None)

        try:
            if search:
                selection = Question.query.order_by(Question.question).filter(Question.question.ilike('%{}%'.format(search))).all()
                if len(selection) is None:
                    abort(404)
                else:
                    current_questions = paginate_questions(request, selection)

                    return jsonify({
                        'success': True,
                        'questions': current_questions,
                        'total_questions': len(selection)
                    })

            else:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category
                )
                question.insert()

                selection = Question.query.order_by(Question.question).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(selection)
                })

        except:
            abort(422)

    """
    @TODO DONE:
    Create a GET endpoint to get questions based on category.
    """
    @app.route('/categories/<int:cat_id>/questions')
    def get_question_by_category(cat_id):

        category = Category.query.filter(Category.id == cat_id).one_or_none()

        selection = Question.query.filter(Question.category == str(cat_id)).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': [c.type for c in Category.query.all()],
            'current_category': category.type
        })

    """
    @TODO DONE:
    Create a POST endpoint to get questions to play the quiz.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        # This endpoint should take category and previous question parameters
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            category_id = quiz_category['id']

            if category_id == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions),
                    Question.category == category_id).all()
            question = None
            if(questions):
                question = random.choice(questions)

            return jsonify({
                'success': True,
                'question': question.format()
            })

        except Exception:
            abort(422)
    """
    @TODO DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    # ERROR HANDLERS
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Operation not allowed'
        }), 405


    @app.errorhandler(422)
    def cannot_process(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Request cannot be processed'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    return app


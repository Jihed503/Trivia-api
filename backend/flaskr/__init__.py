import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS
    # CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Set Access-Control-Allow
    @app.after_request
    def after_request_func(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTION')
        return response

    # Handle GET requests for all available categories
    @app.route('/categories', methods=['GET'])
    def categories():
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        categories_dict = {}
        for category in formatted_categories:
            categories_dict[category['id']] = category['type']
        return jsonify({
            'success': True,
            'categories': categories_dict
        })

    # Handle GET requests for questions
    @app.route('/questions', methods=['GET'])
    def questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]
        categories = Category.query.all()
        current_category = request.args.get('category')

        categories_d = {}
        for category in categories:
            categories_d[category.id] = category.type

        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'current_category': current_category,
            'categories': categories_d
        })

    # Create an endpoint to DELETE question
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(id == question_id)
        question.delete()

        return jsonify({'success': True, 'deleted_question_id': question_id})

    # POST a new question
    @app.route('/questions', methods=['POST'])
    def add_question():
        question = request.json['question']
        answer = request.json['answer']
        category = request.json['category']
        difficulty = request.json['difficulty']

        new_question = Question(question=question, answer=answer,
                                difficulty=difficulty, category=category)

        new_question.insert()

        return jsonify({'success': True, 'added_question_id': new_question.id})

    # Get questions based on a search term
    @app.route('/questions', methods=['POST'])
    def search_question():
        search_term = request.json.get('searchTerm')
        questions = Question.query.filter(
            Question.question.ilike('{}'.format(search_term)))
        count = questions.count()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'search_term': search_term,
            'results_number': count
        })

    # Get questions based on category
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def questions_based_on_category(category_id):
        questions = Question.query.filter(Question.category == category_id)
        formatted_questions = [question.format() for question in questions]
        current_category = Category.query.filter_by(
            id=category_id).first().format()
        count = questions.count()

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        return jsonify({'success': True,
                        'questions': formatted_questions[start:end],
                        'current_category': current_category,
                        'questions_number': count
                        })

    # POST endpoint to get questions to play the quiz
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        category = request.json.get('quiz_category')
        previous_questions = request.json.get('previous_questions')

        if category['id'] != 0:
            questions = [question.format(
            ) for question in Question.query.filter(Question.category == category['id'])]
            if len(questions) == len(previous_questions):
                return jsonify({'success': True, 'quiz_category': category, 'question': None, 'previous_questions': previous_questions})
            elif len(previous_questions) == 0:
                chosen_question = random.choice(questions)
                return jsonify({'success': True, 'quiz_category': category, 'question': chosen_question, 'previous_questions': previous_questions})
            else:
                previous_questions_set = set(previous_questions)
                questions_set = set([question for question in questions])
                questions_left_set = questions_set.difference(questions_set)
                chosen_question = random.choice(questions_left_set)
                return jsonify({'success': True, 'quiz_category': category, 'question': chosen_question, 'previous_questions': previous_questions})
        else:
            questions = [question.format() for question in Question.query]
            if len(questions) == len(previous_questions):
                return jsonify({'success': True, 'quiz_category': category, 'question': None, 'previous_questions': previous_questions})
            elif len(previous_questions) == 0:
                chosen_question = random.choice(questions)
                return jsonify({'success': True, 'quiz_category': category, 'question': chosen_question, 'previous_questions': previous_questions})
            else:
                previous_questions_set = set(previous_questions)
                questions_set = set([question for question in questions])
                questions_left_set = questions_set.difference(questions_set)
                chosen_question = random.choice(questions_left_set)
                return jsonify({'success': True, 'quiz_category': category, 'question': chosen_question, 'previous_questions': previous_questions})

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False, 'error': 400, 'message': 'Bad Request'})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 404, 'message': 'Resources Not Found'})

    @ app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'success': False, 'error': 405, 'message': 'Method Not Allowed'})

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({'success': False, 'error': 422, 'message': 'Unprocessable'})

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'success': False, 'error': 500, 'message': 'Internal Server Error'})
    return app


Dolor consequat minim excepteur aliqua proident reprehenderit eiusmod et elit duis.
Non voluptate minim proident aliqua nisi amet. In aliqua anim qui Lorem magna velit aliquip eu consectetur id quis. Laborum anim est quis cupidatat sunt fugiat minim. Velit non aliqua minim proident laborum fugiat dolor sint dolor aute voluptate. Fugiat elit minim culpa do quis deserunt incididunt laboris sit Lorem. Pariatur non incididunt ut dolore qui elit consectetur nostrud mollit aliqua fugiat fugiat do. Quis ullamco anim eu quis velit consectetur ad minim culpa ex consectetur velit cillum.

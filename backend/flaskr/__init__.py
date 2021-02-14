import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page -1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  selected_questions = questions[start:end]
  return selected_questions

def get_categories():
  categories = Category.query.all()
  formattedCategories = [category.format() for category in categories]
  return formattedCategories


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  
 # Set up CORS. Allow 
  CORS(app)

  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response


  @app.route("/categories", methods=['GET'])
  def recive_categories():
    return  jsonify({
        'success': True,
        'categories': get_categories()
    })

  @app.route('/categories/<int:category_id>/questions/', methods=['GET'])
  def get_questions(category_id):
    selected_question = Question.query.filter_by(category=category_id).all()
    result_per_page =  paginate_questions(request, selected_question)

    question_count = len(Question.query.all())

    if len(result_per_page) == 0 :
        abort(404)
    
    return  jsonify({
        'success': True,
        'pagintated_question': result_per_page,
        'question_count': question_count,
        'current_category': Category.query.get_or_404(category_id).format(),
        'categories': get_categories()
    })


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    question.delete()
    return jsonify({
      'success': True,
      'message':'question has been deleted successfully'
    })
 

  @app.route('/questions', methods=['POST'])
  def store_questiong():
    request_data = request.form
    if len(request_data) >= 2 :

      if 'question' in  request_data and 'answer' in  request_data and 'category_id' in  request_data :

          validatedData = dict(request_data)

          question = Question(
            question = validatedData['question'], 
            answer = validatedData['answer'], 
            category = validatedData['category_id'],
            difficulty = validatedData['difficulty']
          )
      
          question.insert()
      else:
        abort(422)  
    else :
      abort(422)

    return jsonify({
      'success': True,
      'message': 'a New Question Has Been Added Successfully',
      'question':question
    })
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
@app.route('/questions/search', methods=['POST'])
  def question_search():
    request_data = request.form
    if len(request_data) >= 2 :

      if 'question' in  request_data  :

      else:
        abort(422)  
    else :
      abort(422)

    return jsonify({
      'success': True,
      'message': 'the question is found',
      'question':question
    })
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
      }), 422

  @app.errorhandler(422)
  def bad_request(error):
      return jsonify({
              'success': False,
              'error': 400,
              'message': 'bad request'
          }), 400

  @app.errorhandler(500)
  def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'server error'
      }), 500

  return app

    
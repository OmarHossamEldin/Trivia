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
  categories = Category.query.order_by(Category.type).all()
  formattedCategories ={category.id: category.type for category in categories}
  return formattedCategories

def create_app(test_config=None):

  app = Flask(__name__)
  setup_db(app)
  

  CORS(app)

  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

  @app.route("/categories", methods=['GET'])
  def receive_categories():
    return  jsonify({
        'success': True,
        'categories': get_categories()
    })

  @app.route('/questions/', methods=['GET'])
  def get_questions():
    selected_question = Question.query.all()
    result_per_page =  paginate_questions(request, selected_question)

    question_count = len(Question.query.all())
   
    if len(result_per_page) == 0 :
        abort(404)
    
    return  jsonify({
        'success': True,
        'questions': result_per_page,
        'total_questions': question_count,
        'current_category': None,
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
  def store_question():
      requestData = request.get_json()
      if  ('question' in requestData and 'answer' in requestData and 'difficulty' in requestData and 'category_id' in requestData):
          question = Question(question = requestData.get('question'),  answer = requestData.get('answer'), 
                                            category = requestData.get('category_id'), difficulty = requestData.get('difficulty') )
          question.insert()
      else:
        abort(422)  
      return jsonify({
        'success': True,
        'message': 'A New Question Has Been Added Successfully',
        'question':question.id
      })
  
  @app.route('/questions/search', methods=['POST'])
  def question_search():
    validatedData = dict(request.json) 
    if validatedData['searchTerm'] :
          searchterm = validatedData['searchTerm']
          questions = Question.query.filter(Question.question.ilike(f'%{searchterm}%')).all()
          if len(questions)== 0 :
              abort(404)

          formattedQuestions = [question.format() for question in questions]
          return jsonify({
                'success': True,
                'questions': formattedQuestions,
                'total_questions': len(questions),
                'current_category': None
            })
    else :
        return jsonify({
          'success': False,
          'message': 'plz insert term for search',
          'questions': None
        })

    return jsonify({
      'success': True,
      'message': 'the question is found',
      'questions': formattedQuestions
    })

  @app.route('/categories/<int:category_id>/questions/', methods=['GET'])
  def get_categories_questions(category_id):
    selected_question = Question.query.filter_by(category=category_id).all()
    formattedQuestions = [question.format() for question in selected_question]
    if len(formattedQuestions) == 0 :
        abort(404)

    return  jsonify({
        'success': True,
        'questions': formattedQuestions,
      })


  @app.route('/quiz', methods=['POST'])
  def play():
    requestData = request.get_json()
    if  ('quiz_category' in requestData and  'previous_questions' in requestData ):
        category = requestData.get('quiz_category')
        previous_questions = requestData.get('previous_questions')
        if category['type'] == 'click':
          questions = Question.query.all()
        else:
          questions = Question.query.filter_by(category=category['id'] ).all()

        newquestions = Question.query.filter(Question.id.notin_((previous_questions))).all()

        newQuestion = newquestions[random.randrange(
                0, len(newquestions))].format() if len(newquestions) > 0 else None
    else:
      abort(422) 

    return  jsonify({
     'success': True,
     'questions': newQuestion
     })

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

  @app.errorhandler(400)
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

    
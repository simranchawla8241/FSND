import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page=request.args.get('page',1,type=int)
  start=(page -1) * QUESTIONS_PER_PAGE
  end=start + QUESTIONS_PER_PAGE
  formatted_question=[question.format() for question in selection]
  current_questions=formatted_question[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs -Done
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET,POST,PATCH,DELETE,OPTIONS')
    return response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/categories")
  def get_categories():
    categories=Category.query.all()
    formatted_category=[category.format() for category in categories]
    return jsonify({
      'success':True,
      'categories':formatted_category
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route("/questions")
  def get_questions():
    selection=Question.query.all()
    current_questions=paginate_questions(request,selection)

    if len(current_questions)==0:
      abort(404)

    return jsonify({
      'success':True,
      'questions':current_questions,
      'total_questions': len(Question.query.all())
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:qid>",methods=['DELETE'])
  def del_question(qid):
    try:
      quest=Question.query.filter(Question.id==qid).one_or_none()

      if quest is None:
        abort(404)
      
      quest.delete()
      selection=Question.query.order_by(Question.id).all()
      current_questions=paginate_questions(request,selection)

      return jsonify({
      'success':True,
      'deleted':qid,
      'questions':current_questions,
      'total_questions': len(Question.query.all())
    })

    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route("/questions",methods=['POST'])
  def create_question():
    body=request.get_json()
    new_answer=body.get('answer',None)
    new_category=body.get('category',None)
    new_question=body.get('question',None)
    new_difficulty=body.get('difficulty',None)
    
    try:
      question=Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)
      question.insert()

      selection=Question.query.order_by(Question.id).all()
      current_questions=paginate_questions(request,selection)

      return jsonify({
      'success':True,
      'created': question.id,
      'questions':current_questions,
      'total_questions': len(Question.query.all())
    })

    except:
      abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route("/questions/<var>")
  def get_questions_bySubstring(var):
    questions=Question.query.filter(Question.question.contains(var)).all()
    formatted_question=[question.format() for question in questions]
    return jsonify({
      'success':True,
      'questions':formatted_question
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route("/questions/<int:category_id>")
  def get_questions_byCategory(category_id):
    questions=Question.query.filter(Question.category == category_id).all()
    formatted_question=[question.format() for question in questions]
    return jsonify({
      'success':True,
      'questions':formatted_question
    })

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
  # @app.route("/questions/<int:question_id>/category/<int:category_id>",methods=['POST','GET'])
  # def verify_answer(question_id,category_id):
  #   body=request.get_json()
  #   new_answer_entered=body.get('answer',None)

  #   try:
  #     questions=Question.query.filter(Question.id == question_id).one_or_none()
  #     if questions is None:
  #       abort(404)
  #     else:
  #       cat=questions.category
  #       questions_different=Question.query.filter(Question.category == cat).all()
  #       formatted_question=[question.format() for question in questions_different]

  #     if(questions_different.answer==new_answer_entered):
  #       return jsonify({
  #       'success':True,
  #       'Correct':True,
  #       'questions':formatted_question
  #       })
  #     else:
  #       return jsonify({
  #       'success':True,
  #       'Correct':False,
  #       'questions':questions.format()
  #       })
  #   except:
  #     abort(404)

  @app.route('/quizzes', methods=['POST'])
  def play_random_quiz():
    try:
      data = request.get_json()
      print(data)
      #get category id
      category_id = data.get('quiz_category', None)
      #get previous questions 
      previous_questions = data.get('previous_questions', None)
      #print previous question value
      print(previous_questions)
      quiz_questions = Question.query.filter
      (Question.id.notin_(previous_questions)).all()     
      if category_id == 0:
        quiz_questions = Question.query.all()
      else:
        Question.query.filter(Question.id.notin_(previous_questions),
        Question.category == category_id).all()
          
        return jsonify({
                  'success': True,
                  'question': random.randrange(quiz_questions).format() if quiz_questions else None
              })
         
    except Exception as e :
      print(e)
      abort(422)



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success":False,
      "error":404,
      "message":"Resource Not Found"
    }),404

  @app.errorhandler(422)
  def Unprocessable(error):
    return jsonify({
      "success":False,
      "error":422,
      "message":"Unprocessable"
    }),422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success":False,
      "error":400,
      "message":"bad request"
    }),400

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success":False,
      "error":405,
      "message":"method not allowed"
    }),405


  # @app.route('/')
  # def hello_world():
  #   return 'Hello, World1!'
  return app

    
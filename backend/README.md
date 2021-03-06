# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

# API

## Introduction

> this api allows u to store and minpulate questions which you  as data used for trivia game
> every cateogory is a container for the questions  i,e every category has his owen questions
> play game is only about random questions which is stored  with it's answer  and their is randomizer for it without repeating old questions 

## Getting Started

- Base Url 
* localhost
* 127.0.0.1:5000

- Authentication 
* False => you dont have to autherize to use this api

## Errors Handlers

### 404 code
- happens when you look for resource not found
  1.  success': False
  1. error': 404
  1. message   resource not found  
  
### 422 code
- happens when you submit is valid but cant proccess it due to alot of reasons
  1.  success': False
  1. error': 422
  1. message   Unprocessable Entity


### 400 code
- happens when you submit invalid data 
  1.  success': False
  1. error': 400
  1. message   Bad Request

### 500 code
- happens Server error 
  1.  success': False
  1. error: 500
  1. message   server error

## Resources
1. Cateogories
1. Questions

## End Points

- Categories
- categoryQuestions  
    * Method Type GET
    * Url :127.0.0.1:5000/categories/category_id/questions/ 
    * curl --location --request GET '127.0.0.1:5000/categories/1/questions/' 
```
{
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "testing",
            "category": 1,
            "difficulty": 5,
            "id": 26,
            "question": "testing"
        },
        {
            "answer": "testing",
            "category": 1,
            "difficulty": 5,
            "id": 27,
            "question": "testing"
        },
        {
            "answer": "testing",
            "category": 1,
            "difficulty": 5,
            "id": 29,
            "question": "testing"
        },
        {
            "answer": "testing",
            "category": 1,
            "difficulty": 5,
            "id": 30,
            "question": "testing"
        },
    ],
    "success": true
}
```

-  Index
    * Method Type GET
    * Url :127.0.0.1:5000/categories
    * curl --location --request GET 127.0.0.1:5000/categories
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

- Questions
- index  
    * Method Type GET
    * Url :127.0.0.1:5000/questions/?page=1
    * curl --location --request GET 127.0.0.1:5000/questions/?page=1
    * PARAMS  page   1
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        }
    ],
    "success": true,
    "total_questions": 61
}
```

- Delete  
    * Method Type DEL
    * Url :127.0.0.1:5000/questions/37
    * curl --location --request DELETE '127.0.0.1:5000/questions/60'
```
{
    "message": "question has been deleted successfully",
    "success": true
}
```

- Store  
    * Method Type POST
    * Url :127.0.0.1:5000/questions
    * body
    ```
    {
        "question": 123132,
        "answer": 12321,
        "category_id": 2,
        "difficulty": 5
    }
    ```
    * Request
    ```
    curl --location --request POST '127.0.0.1:5000/questions' \
        --data-raw '{
            "question": 123132,
            "answer": 12321,
            "category_id": 2,
            "difficulty": 5
    }'
    ```
```
{
    "message": "question has been deleted successfully",
    "success": true
}
```

- search
    * Method Type POST
    * Url :127.0.0.1:5000/questions/search
    * curl --location --request POST '127.0.0.1:5000questions/search' \ --data-raw '{"searchTerm" :"test"}'
    * Body
```
{
    "searchTerm" :"test"
}
```
```
{
    "current_category": null,
    "questions": [
        {
            "answer": "testing",
            "category": 1,
            "difficulty": 5,
            "id": 26,
            "question": "testing"
        },
        {
            "answer": "testing",
            "category": 1,
            "difficulty": 5,
            "id": 27,
            "question": "testing"
        },
        {
            "answer": "dsfdsf",
            "category": 4,
            "difficulty": 5,
            "id": 57,
            "question": "test5000"
        }
    ],
    "success": true,
    "total_questions": 26
}
```
- Quiz
- playQuiz  
    * Method Type POST
    * Url :127.0.0.1:5000/quiz
    * body
    ```
    {
        "previous_questions":[],
        "quiz_category":{"type":"Science","id":"1"}
    }
    ```
    * Request
    ```
    curl --location --request POST '127.0.0.1:5000/questions' \
        --data-raw '{
        "previous_questions":[],
        "quiz_category":{"type":"Science","id":"1"}
    }'
    ```
```
{
	"questions": {
		"answer": "The Palace of Versailles",
		"category": 3,
		"difficulty": 3,
		"id": 14,
		"question": "In which royal palace would you find the Hall of Mirrors?"
	},
	"success": true
}
```


# Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
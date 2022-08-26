# Trivia API

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1- Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.

2- Delete questions.

3- Add questions and require that they include question and answer text.

4- Search for questions based on a text query string.

5- Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started 

### Pre-requisites and Local Development

Developers using this project should already have:

- Python3 
- Pip 
- node 

#### Backend 

inside the backend folder initialize and activate a virtualenv
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

then run ``` pip install requirements.txt``` All required packages are included in the requirements file.


To run the application run the following commands:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
The application is run on  ``` http://127.0.0.1:5000/``` by default and is a proxy in the frontend configuration.



#### Frontend

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the frontend directory of this repository. After cloning, open your terminal and run:

```
$ npm install
```
The frontend app was built using create-react-app. In order to run the app in development mode use npm start. You can change the script in the package.json file.

```
$ npm start
```
Open http://localhost:3000 to view it in the browser. The page will reload if you make edits.


#### Tests

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


## API Reference

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 404,
    "message": "Resource not found"
}
```

The API will return one of these error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Not Processable
405: Method Not Allowed

### Endpoints


**GET /categories**

General:
- Returns a list of categories, success value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

Sample: ```curl http://127.0.0.1:5000/categories```

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

**DELETE /questions/{id}**

General:
- Deletes the question of the given ID if it exists. Returns success value.

Sample ```curl -X DELETE http://127.0.0.1:5000/questions/16?page=2 ```


```
{
  "success": true
}
```

**POST /questions/{id}**


General:
- Creates a new question using the submitted title, answer, category and difficulty. Returns the id of the created question id, success value, total questions number, and questions list based on current page number to update the frontend

Sample: ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What was the name of the first man-made satellite launched by the Soviet Union in 1957?", "answer": "Sputnik 1","category" :"1", "difficulty":"2"}'```


```
{
  "created": 68, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": "5", 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": "4", 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": "5", 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": "4", 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": "6", 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": "6", 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": "4", 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": "3", 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": "3", 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": "3", 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 61
}
```


**POST /search**


General:
- search for a question using the submitted search term. Returns the results, success value, total questions.


Sample ```curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"who"}'```

```
{
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": "4", 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": "4", 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": "1", 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

**GET /categories/{id}/questions**


General:

- Returns a list of questions, in the given category, category total_questions and success value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.


Sample: ```curl http://127.0.0.1:5000/categories/3/questions```

```
{
  "current_category": "Geography", 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": "3", 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": "3", 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": "3", 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

**POST /quizzes**

General:
- recive the actual question and the category
- return the next question in the same category and success value.


Sample``` curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Geography","id":"3"}, "previous_questions":[13]}'``` 


```
{
  "question": {
    "answer": "Agra", 
    "category": "3", 
    "difficulty": 2, 
    "id": 15, 
    "question": "The Taj Mahal is located in which Indian city?"
  }, 
  "success": true
}
```



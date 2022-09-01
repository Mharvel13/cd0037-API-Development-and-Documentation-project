# Trivia API DOCUMENTATION

The following is a the expected endpoints that are expected when called.


##  GET ALL CATEGORIES ENDPOINT

GET  '/categories'
- Fetches all categories where the keys value pairs are the ids and the corresponding string of the category 
- Example Response:

  ```json
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

##  GET ALL QUESTIONS ENDPOINT

GET '/questions'
- Fetches a paginated dictionary of questions of all available categories 
- Example Response:

```json
        {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "current_category": "Null",
        "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
        ],
        "total_questions": 21
    }
```

## DELETE A QUESTION ENDPOINT

DELETE '/questions/<int:question_id>'

- Deletes a question by a specified id number (only the question with that id exists) 
. Request Arguments: question_id 
- Example Request: DELETE 'http://127.0.0.1:5000/questions/9'
- Example Response:
 ```json
    {
        "deleted_question": 9,
        "success": true
    }

```


##  CREATE A NEW QUESTION ENDPOINT

POST '/questions'
- Creates a new question using the submitted question and answer text, difficulty and category score 
- Request Arguments: answer, category, difficulty, question 
- Example Response:

```json
    {
      "success": true
    }

```

##  SEARCH FOR A QUESTION ENDPOINT

POST '/questions/search'
- Fetches all questions where a substring matches the search_term. 
- Request Arguments: search_term 
- Example Response:

```json
    {
    "current_category": "Null",
    "questions": [
        {
             "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
           "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
        "success": true,
        "total_questions": 2
    }
```


##  GET QUESTIONS BY CATEGORY ENDPOINT

GET '/categories/<int:category_id>/questions'
- Fetches all questions where the category matches the category_id . Request Arguments: category_id . 
- Example Request: 'http://127.0.0.1:5000/categories/2/questions'
- Example Response:

```json
    {
    "current_category": "Art",
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
    ],
  "success": true,
  "total_questions": 4
}

```

##  PLAY QUIZ ENDPOINT

POST '/quizzes'
- Fetches a random question to play the quiz
- Request Arguments: previous_questions, quiz_category
- Example Response:

```json
    {
        "question": 
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        }
  }

```
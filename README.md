Quiz Application API Documentation
Table of Contents
Overview

Authentication API

User Login

User Registration

Admin Registration

User Actions API

Get All Active Quizzes

Attempt a Quiz

Get Quiz Attempts

Admin Actions API

Category Management

Quiz Management

Question Management

Submission Management

Examples

Error Handling

Overview
This document describes the complete API for a Quiz Application with user and admin functionality. The API supports:

User authentication and authorization

Quiz taking functionality for regular users

Quiz management for admin users

Comprehensive error handling

All endpoints require token authentication (except login/registration) with the token included in the Authorization header:

Copy
Authorization: Token <your_token>
Authentication API
1. User Login
Endpoint: POST /api/login

Description: Authenticates a user and returns an authentication token.

Request Body:

json
Copy
{
    "username": "user@example.com",
    "password": "securepassword123"
}
Response:

json
Copy
{
    "status": true,
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
2. User Registration
Endpoint: POST /api/register_user

Description: Creates a new regular user account with 'user' role.

Request Body:

json
Copy
{
    "email": "newuser@example.com",
    "password": "newpassword123"
}
3. Admin Registration
Endpoint: POST /api/register_admin

Description: Creates a new admin account with 'admin' role.

Request Body:

json
Copy
{
    "email": "admin@example.com",
    "password": "adminpass123"
}
User Actions API
1. Get All Active Quizzes
Endpoint: GET /api/get_all_quiz

Description: Retrieves all active quizzes available for the authenticated user.

Response:

json
Copy
{
    "quiz": [list of quiz objects],
    "questions": [list of question objects]
}
2. Attempt a Quiz
Endpoint: POST /api/attempt_quiz

Request Body:

json
Copy
{
    "quiz_id": 1,
    "answers": [
        {"question": 1, "selected_option": 2},
        {"question": 2, "selected_option": 1}
    ]
}
Success Response:

json
Copy
{
    "status": true,
    "message": "Quiz attempted successfully",
    "score": 85
}
3. Get Quiz Attempts
Endpoint: GET /api/get_quiz_attempts

Description: Retrieves the user's quiz attempt history.

Admin Actions API
Category Management
POST /api/admin/add_categories - Create new categories

GET /api/admin/get_categories - List all categories

PATCH /api/admin/update_category - Update categories

Quiz Management
POST /api/admin/add_quiz - Create new quizzes

GET /api/admin/get_quiz - List all quizzes

PATCH /api/admin/update_quiz - Update quizzes

Question Management
POST /api/admin/add_question - Add questions

json
Copy
{
    "quiz_id": 1,
    "question_text": "What is 2+2?",
    "option1": "1",
    "option2": "2",
    "option3": "3",
    "option4": "4",
    "answer": 4,
    "marks": 5
}
Submission Management
GET /api/admin/get_quiz_submissions - View quiz submissions

GET /api/admin/get_all_submissions - View all submissions

Examples
User Login
bash
Copy
curl -X POST http://localhost:8000/api/login \
-H 'Content-Type: application/json' \
-d '{"username":"user@example.com","password":"pass123"}'
Attempt Quiz
bash
Copy
curl -X POST http://localhost:8000/api/attempt_quiz \
-H 'Authorization: Token your_token' \
-H 'Content-Type: application/json' \
-d '{"quiz_id":1,"answers":[{"question":1,"selected_option":2}]}'
Error Handling
All endpoints return consistent error responses:

json
Copy
{
    "status": false,
    "message": "Descriptive error message"
}
Common error scenarios:

Missing required fields

Invalid credentials

Unauthorized access

Resource not found

Validation errors

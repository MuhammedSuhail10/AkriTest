from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import *
from .serializers import *

User = get_user_model()

# Categories
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_categories(request):
    """
        Create a new category (Admin only)
        This endpoint allows authenticated admin users to create new categories.

        Parameters:
        - name (string, required): The name of the category to be created
        
        Returns:
        - JSON response indicating success/failure:
            - If successful: {'status': True, 'message': 'Category added successfully'}
            - If failed: 
                - {'status': False, 'message': 'You are not authorized...'} (for non-admin users)
                - {'status': False, 'message': 'Category already exists'} (if category exists)
                - {'status': False, 'message': 'Name is required'} (if name missing)
        
        Permissions:
        - User must be authenticated
        - User must have 'admin' role
    """

    user = request.user
    if user.role != 'admin':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    if request.data.get('name'):
        name = request.data.get('name')
        if not Category.objects.filter(name=name, created_by=user).exists():
            category = Category.objects.create(name=name, created_by=user)
            category.save()
            return Response({'status':True, 'message': 'Category added successfully'})
        return Response({'status':False, 'message': 'Category already exists'})
    return Response({'status':False, 'message': 'Name is required'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    user = request.user
    if user.role != 'admin':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    categories = Category.objects.filter(created_by=user)
    serializer = CategorySerial(categories, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_category(request):
    if not request.GET.get('category_id'):
        return Response({'status':False, 'message': 'Category ID is required'})
    id = request.GET.get('category_id')
    user = request.user
    if user.role != 'admin':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    if Category.objects.filter(id=id, created_by=user).exists():
        category = Category.objects.get(id=id, created_by=user)
        serializer = CategorySerial(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True, 'message': 'Category updated successfully'})
        return Response(serializer.errors)
    return Response({'status':False, 'message': 'Category not found'})

# Quizes
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_quiz(request):
    """
        Create a new quiz (Admin only)
        This endpoint allows authenticated admin users to create new quizzes.

        Body:
        - category_id (int, required): The ID of the category to which the quiz belongs
        - name (string, required): The name of the quiz to be created

        Returns:
        - JSON response indicating success/failure:
            - If successful: {'status': True, 'message': 'Quiz added successfully'}
            - If failed: 
                - {'status': False, 'message': 'You are not authorized...'} (for non-admin users)
                - {'status': False, 'message': 'Quiz already exists'} (if quiz exists)
                - {'status': False, 'message': 'Category ID is required'} (if category_id missing)
        
        Permissions:
        - User must be authenticated
        - User must have 'admin' role

        Example:
        POST /api/admin/add_quiz
        {
            "name": "Sample Quiz",
            "category_id": 1
        }
    """

    user = request.user
    if user.role != 'admin':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    if not request.data.get('category_id'):
        return Response({'status':False, 'message': 'Category ID is required'})
    if not Quiz.objects.filter(name=name, created_by=user).exists():
        serializer = AddQuizSerial(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=user, category_id=request.data.get('category_id'))
            return Response({'status':True, 'message': 'Quiz added successfully'})
        return Response(serializer.errors)
    return Response({'status':False, 'message': 'Quiz already exists'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quiz(request):
    user = request.user
    if user.role != 'admin':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    quizzes = Quiz.objects.filter(created_by=user)
    serializer = QuizSerial(quizzes, many=True)
    return Response(serializer.data)

# Can be used to change is_active status of quiz
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_quiz(request):
    if not request.GET.get('quiz_id'):
        return Response({'status':False, 'message': 'Quiz ID is required'})
    id = request.GET.get('quiz_id')
    user = request.user
    if user.role != 'admin':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    if Quiz.objects.filter(id=id, created_by=user).exists():
        quiz = Quiz.objects.get(id=id, created_by=user)
        serializer = QuizSerial(quiz, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True, 'message': 'Quiz updated successfully'})
        return Response(serializer.errors)
    return Response({'status':False, 'message': 'Quiz not found'})

# Questions
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_question(request):
    """
        Create a new question (Admin only)
        This endpoint allows authenticated admin users to create new questions for a quiz.

        Body:
        - quiz_id (int, required): The ID of the quiz
        - question_text (string, required): 
        - option1 (string, required): 
        - option2 (string, required): 
        - option3 (string, required): 
        - option4 (string, required): 
        - answer (string, required): 
        - marks (string, required): 

        Returns:
        - JSON response indicating success/failure:
            - if successful: {'status': True, 'message': 'Question added successfully'}
            - if failed:
                - {'status': False, 'message': 'You are not authorized...'} (for non-admin users)
                - {'status': False, 'message': 'Quiz not found'} (if quiz not found)
                - {'status': False, 'message': 'Quiz ID is required'} (if quiz_id missing)
        
        Permissions:
        - User must be authenticated
        - User must have 'admin' role

        Example:
        POST /api/admin/add_question
        {
            "quiz_id": 1,
            "question_text": "What is the capital of France?",
            "option1": "Berlin",
            "option2": "Madrid",
            "option3": "Paris",
            "option4": "Rome",
            "answer": 3,
            "marks": 5
        }
    """

    user = request.user
    if user.role != 'admin':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    if request.data.get('quiz_id'):
        quiz_id = request.data.get('quiz_id')
        if Quiz.objects.filter(id=quiz_id, created_by=user).exists():
            quiz = Quiz.objects.get(id=quiz_id, created_by=user)
            serializer = QuestionSerial(data=request.data)
            if serializer.is_valid():
                serializer.save(quiz_id=quiz_id, is_active=True)
                return Response({'status':True, 'message': 'Question added successfully'})
            return Response(serializer.errors)
        return Response({'status':False, 'message': 'Quiz not found'})
    return Response({'status':False, 'message': 'Quiz ID is required'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_question(request):
    user = request.user
    if user.role != 'admin':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    if request.GET.get('quiz_id'):
        quiz_id = request.GET.get('quiz_id')
        if Quiz.objects.filter(id=quiz_id).exists():
            questions = Question.objects.filter(quiz_id=quiz_id)
            serializer = QuestionSerial(questions, many=True)
            return Response(serializer.data)
        return Response({'status':False, 'message': 'Quiz not found'})
    return Response({'status':False, 'message': 'Quiz ID is required'})

# Can be used to change is_active status of question
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_question(request):
    user = request.user
    if user.role != 'admin':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    if not request.GET.get('quiz_id'):
        return Response({'status':False, 'message': 'Quiz ID is required'})
    id = request.GET.get('quiz_id')
    if Question.objects.filter(id=id).exists():
        question = Question.objects.get(id=id)
        serializer = QuestionSerial(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True, 'message': 'Question updated successfully'})
        return Response(serializer.errors)
    return Response({'status':False, 'message': 'Question not found'})

# Submissions
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quiz_submissions(request):
    user = request.user
    if user.role != 'admin':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    if request.GET.get('quiz_id'):
        quiz_id = request.GET.get('quiz_id')
        if Quiz.objects.filter(id=quiz_id).exists():
            submissions = QuizAttempt.objects.filter(quiz_id=quiz_id)
            serializer = AttemptSerial(submissions, many=True)
            return Response(serializer.data)
        return Response({'status':False, 'message': 'Quiz not found'})
    return Response({'status':False, 'message': 'Quiz ID is required'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_submissions(request):
    user = request.user
    if user.role != 'admin':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    submissions = QuizAttempt.objects.filter(quiz__created_by=user)
    serializer = AttemptSerial(submissions, many=True)
    return Response(serializer.data)
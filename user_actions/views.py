from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from admin_actions.models import *
from admin_actions.serializers import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_quiz(request):
    user = request.user
    if user.role != 'user':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    quizzes = Quiz.objects.filter(is_active=True)
    serializer = QuizSerial(quizzes, many=True)
    questions = Question.objects.filter(quiz__in=quizzes, is_active=True)
    question_serializer = QuestionSerial(questions, many=True)
    return Response({"quiz": serializer.data, "questions": question_serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def attempt_quiz(request):
    """
        Attempt a quiz.
        This endpoint allows a user to attempt a quiz by submitting their answers.

        Body:
        - quiz_id (int, required): The ID of the quiz
        - answers (list, required): A list of dictionaries containing the question ID and selected option.
            Example: [{"question": 1, "selected_option": 2}, {"question": 2, "selected_option": 1}]

        Returns:
        - JSON response indicating success/failure:
            - if success: {'status': True, 'message': 'Quiz attempted successfully', 'score': score}
            - if failure: {'status': False, 'message': 'Error message'}
        
        Permissions:
        - User must be authenticated
        - User must have 'user' role
        - User must not have already attempted the quiz
        - Quiz must exist and be active
        - Answers must be provided in the correct format

        Example:
        POST /api/attempt_quiz
        {
            "quiz_id": 1,
            "answers": [
                {"question": 1, "selected_option": 2},
                {"question": 2, "selected_option": 1}
            ]
        }
    """

    user = request.user
    if user.role != 'user':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    if not request.data.get('quiz_id'):
        return Response({'status':False, 'message': 'Quiz ID is required'})
    quiz_id = request.data.get('quiz_id')
    if Quiz.objects.filter(id=quiz_id).exists():
        if not QuizAttempt.objects.filter(user=user, quiz__id=quiz_id).exists():
            quiz = Quiz.objects.get(id=quiz_id)
            questions = Question.objects.filter(quiz=quiz, is_active=True)
            answers = request.data.get('answers')
            score = 0
            for answer in answers:
                if questions.filter(id=answer['question']).exists():
                    question = questions.get(id=answer['question'])
                    if answer.get('selected_option') == question.get_answer():
                        score += question.marks
            attempt = QuizAttempt.objects.create(user=user, quiz=quiz, score=score)
            attempt.save()
            return Response({'status':True, 'message': 'Quiz attempted successfully', 'score': score})
        return Response({'status':False, 'message': 'You have already attempted this quiz'})
    return Response({'status':False, 'message': 'Quiz not found'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quiz_attempts(request):
    user = request.user
    if user.role != 'user':
        return Response({'status':False, 'message': 'You are not authorized to perform this action'})
    attempts = QuizAttempt.objects.filter(user=user)
    serializer = AttemptSerial(attempts, many=True)
    return Response(serializer.data)
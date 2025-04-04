from rest_framework import serializers
from .models import *

class CategorySerial(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AddQuizSerial(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        exclude = ['created_by', 'category']

class QuizSerial(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class QuestionSerial(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ['quiz']

class AddAttemptSerial(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        exclude = ['user', 'quiz']

class AttemptSerial(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = '__all__'
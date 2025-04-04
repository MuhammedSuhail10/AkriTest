from django.contrib import admin
from .models import Category, Quiz, Question, QuizAttempt

admin.site.register(QuizAttempt)
admin.site.register(Question)
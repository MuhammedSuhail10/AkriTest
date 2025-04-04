from django.urls import path
from .views import *

urlpatterns = [
    path('get_all_quiz', get_all_quiz),
    path('attempt_quiz', attempt_quiz),
    path('get_quiz_attempts', get_quiz_attempts),
]
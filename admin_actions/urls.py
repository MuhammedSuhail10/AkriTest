from django.urls import path
from .views import *

urlpatterns = [
    path('add_categories', add_categories),
    path('get_categories', get_categories),
    path('update_category', update_category),
    path('add_quiz', add_quiz),
    path('get_quiz', get_quiz),
    path('update_quiz', update_quiz),
    path('add_question', add_question),
    path('get_question', get_question),
    path('update_question', update_question),
    path('get_all_submissions',get_all_submissions),
    path('get_quiz_submissions',get_quiz_submissions),
]
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    option1 = models.CharField("Option 1", max_length=255)
    option2 = models.CharField("Option 2", max_length=255)
    option3 = models.CharField("Option 3", max_length=255)
    option4 = models.CharField("Option 4", max_length=255)
    answer = models.IntegerField(choices=[(1, "Option 1"),(2, "Option 2"),(3, "Option 3"),(4, "Option 4"),])
    marks = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text[:50]

    def get_answer(self):
        return getattr(self, f"option{self.answer}")

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    attempted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.name}"
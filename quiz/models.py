from django.contrib.auth.models import User
from django.db import models
from random import randint

class StatusManager(models.Manager):
    def get_or_create(self, user):
        user = user if user.is_authenticated else User.objects.get(username='placeholder')
        try:
            return self.get(user=user)
        except self.model.DoesNotExist:
            return self.create(user=user)

class Status(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question_difficulty = models.IntegerField(default=1)
    answer_difficulty = models.IntegerField(default=1)
    matches_played = models.IntegerField(default=0)
    matches_won = models.IntegerField(default=0)
    matches_per_round = models.IntegerField(default=5)
    objects = StatusManager()

    def increase_difficulty(self):
        pass

    def decrease_difficulty(self):
        pass

class QuestionManager(models.Manager):
    def random_question(self, status):
        try:
            question_count = self.filter(difficulty=status.question_difficulty).count()
            if question_count == 0:
                return None
            random_index = randint(0, question_count - 1)
            return self.filter(difficulty=status.question_difficulty)[random_index]
        except self.model.DoesNotExist:
            return None

class Question(models.Model):
    text = models.TextField()
    difficulty = models.IntegerField(default=1)
    objects = QuestionManager()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    difficulty = models.IntegerField(default=1)

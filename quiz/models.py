from django.contrib.auth.models import User
from django.db import models
from random import randint


class QuestionManager(models.Manager):
    def random_question(self, status):
        try:
            question_count = self.filter(difficulty=status.question_difficulty).count()
            if question_count == 0:
                raise self.model.DoesNotExist(f'No questions found with difficulty {status.question_difficulty}')
            random_index = randint(0, question_count - 1)
            return self.filter(difficulty=status.question_difficulty)[random_index]
        except self.model.DoesNotExist:
            raise self.model.DoesNotExist('No questions found')

class Question(models.Model):
    text = models.TextField(unique=True)
    difficulty = models.IntegerField(default=1)
    objects = QuestionManager()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    difficulty = models.IntegerField(default=1)

class StatusManager(models.Manager):
    def get_or_create(self, user):
        user = user if user.is_authenticated else User.objects.get(username='placeholder')
        try:
            return self.get(user=user)
        except self.model.DoesNotExist:
            return self.create(user=user)

class Status(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question_difficulty = models.IntegerField(default=6)
    answer_difficulty = models.IntegerField(default=6)
    matches_played = models.IntegerField(default=0)
    matches_won = models.IntegerField(default=0)
    matches_per_round = models.IntegerField(default=2)
    objects = StatusManager()

    def increase_difficulty(self):
        max_difficulty = Question.objects.aggregate(models.Max('difficulty'))['difficulty__max']
        if self.question_difficulty < max_difficulty:
            self.question_difficulty += 1

    def decrease_difficulty(self):
        min_difficulty = Question.objects.aggregate(models.Min('difficulty'))['difficulty__min']
        if self.question_difficulty > min_difficulty:
            self.question_difficulty -= 1

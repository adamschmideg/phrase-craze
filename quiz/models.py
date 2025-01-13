from django.db import models
from random import randint

class QuestionManager(models.Manager):
    def random_for_status(self, status):
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

class Status(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question_difficulty = models.IntegerField(default=1)
    answer_difficulty = models.IntegerField(default=1)
    matches_played = models.IntegerField(default=0)
    matches_per_round = models.IntegerField(default=5)

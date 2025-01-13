from django.db import models

class Question(models.Model):
    text = models.TextField()
    difficulty = models.IntegerField(default=1)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField()
    difficulty = models.IntegerField(default=1)

class Status(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question_difficulty = models.IntegerField()
    answer_difficulty = models.IntegerField()
    match_in_round_index = models.IntegerField()

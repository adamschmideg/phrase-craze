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
            status = self.get(user=user)
        except self.model.DoesNotExist:
            status = self.create(user=user)

        status.set_lowest_difficulty()
        return status

class Status(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question_difficulty = models.IntegerField(default=6)
    answer_difficulty = models.IntegerField(default=6)
    matches_played = models.IntegerField(default=0)
    matches_won = models.IntegerField(default=0)
    matches_per_round = models.IntegerField(default=2)
    objects = StatusManager()

    def set_lowest_difficulty(self):
        self.question_difficulty = Question.objects.aggregate(models.Min('difficulty'))['difficulty__min']
        # find questions with the lowest difficulty
        questions = Question.objects.filter(difficulty=self.question_difficulty)
        # find answers with the lowest difficulty that belong to the questions
        self.answer_difficulty = Answer.objects.filter(question__in=questions).aggregate(models.Min('difficulty'))['difficulty__min']

    def adjust_difficulty(self, increase=True):
        # Get all distinct difficulty values
        difficulties = list(Question.objects.values_list('difficulty', flat=True).distinct())

        # Sort difficulties based on whether we're increasing or decreasing
        difficulties.sort(reverse=not increase)

        # Find the next difficulty level
        for difficulty in difficulties:
            if increase and difficulty > self.question_difficulty:
                self.question_difficulty = difficulty
                return
            if not increase and difficulty < self.question_difficulty:
                self.question_difficulty = difficulty
                return

        # If no suitable difficulty is found, don't change the difficulty



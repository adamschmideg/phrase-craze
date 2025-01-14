import random
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms.models import model_to_dict

from quiz import models

PROMOTE_AT_RATIO = 0.8
DEMOTE_AT_RATIO = 0.5

def home(request):
    status = models.Status.objects.get_or_create(request.user)
    question = models.Question.objects.random_question(status)
    return redirect(reverse('show_question', kwargs={'quiz_id': 0, 'question_id': question.id}))

def show_question(request, quiz_id, question_id):
    status = model_to_dict(models.Status.objects.get_or_create(request.user))
    question = models.Question.objects.get(id=question_id)
    answer_ids = ','.join([str(answer.id) for answer in question.answers.all()])
    answers_url = reverse('show_answers', kwargs={'quiz_id': quiz_id, 'question_id': question_id, 'answer_ids': answer_ids})
    return render(request, 'quiz/question.html', {'question': question, 'answers_url': answers_url, 'status': status})

def show_answers(request, quiz_id, question_id, answer_ids):
    answers = models.Answer.objects.filter(id__in=answer_ids.split(','))
    return render(request, 'quiz/answers.html', {'quiz_id': quiz_id, 'question_id': question_id, 'answers': answers})

def submit_answer(request, quiz_id, question_id, answer_id):
    if request.method == 'POST':
        answer = models.Answer.objects.get(id=answer_id)
        status = models.Status.objects.get_or_create(request.user)

        status.matches_played += 1
        if answer.is_correct:
            status.matches_won += 1
        if status.matches_played == status.matches_per_round:
            if status.matches_won / status.matches_per_round >= PROMOTE_AT_RATIO:
                status.increase_difficulty()
            elif status.matches_won / status.matches_per_round <= DEMOTE_AT_RATIO:
                status.decrease_difficulty()
            status.matches_won = 0
            status.matches_played = 0
        status.save()

        next_question = models.Question.objects.random_question(status)
        return redirect(reverse('show_question', kwargs={'quiz_id': quiz_id, 'question_id': next_question.id}))


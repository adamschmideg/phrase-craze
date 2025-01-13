import random
from django.shortcuts import render, redirect
from django.urls import reverse
from quiz import models

def home(request):
    return redirect(reverse('show_question', kwargs={'quiz_id': 0, 'question_id': 0}))

def show_question(request, quiz_id, question_id):
    question = models.Question.objects.get(id=question_id)
    answer_ids = ','.join([str(answer.id) for answer in question.answers.all()])
    answers_url = reverse('show_answers', kwargs={'quiz_id': quiz_id, 'question_id': question_id, 'answer_ids': answer_ids})
    return render(request, 'quiz/question.html', {'question': question, 'answers_url': answers_url})

def show_answers(request, quiz_id, question_id, answer_ids):
    question = models.Question.objects.get(id=question_id)
    answers = question.answers.all()
    return render(request, 'quiz/answers.html', {'quiz_id': quiz_id, 'question_id': question_id, 'answers': answers})

def submit_answer(request, quiz_id, question_id, answer_id):
    if request.method == 'POST':
        answer = models.Answer.objects.get(id=answer_id)
        if answer.is_correct:
            # TODO: Score
            pass

        question_count = models.Question.objects.count()
        next_question_id = random.randint(0, question_count - 1)
        return redirect(reverse('show_question', kwargs={'quiz_id': quiz_id, 'question_id': next_question_id}))


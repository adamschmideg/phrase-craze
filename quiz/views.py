from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.forms.models import model_to_dict

from quiz import forms, models

PROMOTE_AT_RATIO = 0.8
DEMOTE_AT_RATIO = 0.5

def prepare_home(request):
    status = models.Status.objects.get_or_create(request.user)
    question = models.Question.objects.random_question(status)
    return reverse('show_question', kwargs={'quiz_id': 0, 'question_id': question.id})

def home(request):
    redirect_to = prepare_home(request)
    return redirect(redirect_to)

def show_question(request, quiz_id, question_id):
    status = model_to_dict(models.Status.objects.get_or_create(request.user))
    question = models.Question.objects.get(id=question_id)
    answer_ids = ','.join([str(answer.id) for answer in question.answers.all()])
    answers_url = reverse('show_answers', kwargs={'quiz_id': quiz_id, 'question_id': question_id, 'answer_ids': answer_ids})
    return render(request, 'quiz/question.html', {'question': question, 'answers_url': answers_url, 'status': status})

def show_answers(request, quiz_id, question_id, answer_ids):
    answers = models.Answer.objects.filter(id__in=answer_ids.split(','))
    return render(request, 'quiz/answers.html', {'quiz_id': quiz_id, 'question_id': question_id, 'answers': answers})

def prepare_submit_answer(request, quiz_id, question_id, answer_id):
    if request.method == 'POST':
        answer = models.Answer.objects.get(id=answer_id)
        status = models.Status.objects.get_or_create(request.user)

        status.matches_played += 1
        if answer.is_correct:
            status.matches_won += 1
        if status.matches_played == status.matches_per_round:
            if status.matches_won / status.matches_per_round >= PROMOTE_AT_RATIO:
                status.adjust_difficulty(increase=True)
            elif status.matches_won / status.matches_per_round <= DEMOTE_AT_RATIO:
                status.adjust_difficulty(increase=False)
            status.matches_won = 0
            status.matches_played = 0
        status.save()

        next_question = models.Question.objects.random_question(status)
        return 'show_question', {'quiz_id': quiz_id, 'question_id': next_question.id}

def submit_answer(request, quiz_id, question_id, answer_id):
    view_name, context = prepare_submit_answer(request, quiz_id, question_id, answer_id)
    redirect_to = reverse(view_name, kwargs=context)
    return redirect(redirect_to)

def edit_status(request, user_id):
    status = get_object_or_404(models.Status, user_id=user_id)

    if request.method == 'POST':
        form = forms.StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('status_detail', status_id=status.id)
    else:
        form = forms.StatusForm(instance=status)

    return render(request, 'quiz/edit_status.html', {'form': form, 'status': status})

def status_detail(request, user_id):
    status = get_object_or_404(models.Status, user_id=user_id)
    return render(request, 'quiz/status_detail.html', {'status': status})



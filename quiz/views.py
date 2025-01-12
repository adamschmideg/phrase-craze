import random
from django.shortcuts import render, redirect
from django.urls import reverse

quizzes = {
    0: {
        'questions': {
            0: {
                'question_id': 0,
                'text': 'The quick brown fox jumps over the lazy dog.',
                'answers': [
                    {'answer_id': 0, 'text': 'jumps over the lazy dog.', 'correct': True},
                    {'answer_id': 1, 'text': 'jumps over the dog!', 'correct': False},
                    {'answer_id': 2, 'text': 'jumps over a lazy dog.', 'correct': False},
                    {'answer_id': 3, 'text': 'jumps over the lazy cat.', 'correct': False}
                ]
            },
            1: {
                'question_id': 2,
                'text': 'A stitch in time saves nine.',
                'answers': [
                    {'answer_id': 0, 'text': 'saves nine.', 'correct': True},
                    {'answer_id': 1, 'text': 'saves time.', 'correct': False},
                    {'answer_id': 2, 'text': 'saves a stitch.', 'correct': False},
                    {'answer_id': 3, 'text': 'saves a stitch in time.', 'correct': False}
                ]
            },
        }
    }
}

def home(request):
    return redirect(reverse('show_question', kwargs={'quiz_id': 0, 'question_id': 0}))

def show_question(request, quiz_id, question_id):
    question = quizzes[quiz_id]['questions'][question_id]
    answer_ids = ','.join(str(answer['answer_id']) for answer in question['answers'])
    answers_url = reverse('show_answers', kwargs={'quiz_id': quiz_id, 'question_id': question_id, 'answer_ids': answer_ids})
    return render(request, 'quiz/question.html', {'question': question, 'answers_url': answers_url})

def show_answers(request, quiz_id, question_id, answer_ids):
    question = quizzes[quiz_id]['questions'][question_id]
    answers = [question['answers'][int(i)] for i in answer_ids.split(',')]
    return render(request, 'quiz/answers.html', {'quiz_id': quiz_id, 'question_id': question_id, 'answers': answers})

def submit_answer(request, quiz_id, question_id, answer_id):
    if request.method == 'POST':
        question = quizzes[quiz_id]['questions'][question_id]
        answer = question['answers'][answer_id]
        if answer['correct']:
            # TODO: Score
            pass

        question_ids = list(quizzes[quiz_id]['questions'].keys())
        next_question_id = random.randint(0, len(question_ids) - 1)
        return redirect(reverse('show_question', kwargs={'quiz_id': quiz_id, 'question_id': next_question_id}))


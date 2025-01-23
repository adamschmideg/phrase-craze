from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from quiz import views
from .models import Answer, Question, Status

class PrepareShowAnswersTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # self.user = AnonymousUser()

        # Create some test answers
        self.user = User.objects.create_user(username='placeholder', password='12345')

    def test_prepare_show_answers(self):
        question1 = Question.objects.create(text="Question 1", difficulty=1)
        answer1 = Answer.objects.create(question_id=question1.id, text="Answer 1", is_correct=True)

        _ = Question.objects.create(text="Question 1", difficulty=2)

        status = Status.objects.get_or_create(self.user)
        status.question_difficulty = 1
        status.matches_per_round = 1
        status.save()

        request = self.factory.get('/dummy/')
        request.user = self.user
        request.method = 'POST'

        quiz_id = 1
        template_name, context = views.prepare_submit_answer(request, quiz_id, question1.id, answer1.id)

        next_question = Question.objects.get(pk=context['question_id'])
        self.assertEqual(next_question.difficulty, 2)

    def test_skip_missing_difficulty(self):
        question1 = Question.objects.create(text="Question 1", difficulty=1)
        answer1 = Answer.objects.create(question_id=question1.id, text="Answer 1", is_correct=True)

        question2 = Question.objects.create(text="Question 1", difficulty=3)

        status = Status.objects.get_or_create(self.user)
        status.question_difficulty = 1
        status.matches_per_round = 1
        status.save()
        status.adjust_difficulty(increase=True)
        self.assertEqual(status.question_difficulty, question2.difficulty, "Increase difficulty should skip missing difficulties")
        status.adjust_difficulty(increase=False)
        self.assertEqual(status.question_difficulty, question1.difficulty, "Decrease difficulty should skip missing difficulties")

        request = self.factory.get('/dummy/')
        request.user = self.user
        request.method = 'POST'

        quiz_id = 1
        template_name, context = views.prepare_submit_answer(request, quiz_id, question1.id, answer1.id)

        next_question = Question.objects.get(pk=context['question_id'])
        self.assertEqual(next_question.difficulty, question2.difficulty)



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
        answer1 = Answer.objects.create(question_id=question1.id, text="Answer 1")

        question2 = Question.objects.create(text="Question 1", difficulty=2)
        answer2 = Answer.objects.create(question_id=question2.id, text="Answer 1")

        status = Status.objects.get_or_create(self.user)
        status.question_difficulty = 1
        status.save()

        request = self.factory.get('/')
        request.user = self.user
        views.prepare_home(request)

        request.method = 'POST'

        # Call the prepare function
        quiz_id = 1
        question_id = 1
        answer_id = 1
        template_name, context = views.prepare_submit_answer(request, quiz_id, question_id, answer_id)

        next_question = Question.objects.get(pk=context['question_id'])
        self.assertEqual(next_question.difficulty, 2)



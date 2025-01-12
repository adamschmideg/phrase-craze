from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/', views.show_question, name='show_question'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/answers/<str:answer_ids>/', views.show_answers, name='show_answers'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/answer/<int:answer_id>/', views.submit_answer, name='submit_answer'),
]

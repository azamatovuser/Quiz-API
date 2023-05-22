from django.urls import path
from .views import CategoryListAPIView, QuestionListAPIView, ResultListAPIView, AnswerFromStudentPostAPIView


urlpatterns = [
    path('category/', CategoryListAPIView.as_view()),
    path('category/<int:category_id>/question/', QuestionListAPIView.as_view()),
    path('result/', ResultListAPIView.as_view()),
    path('answer_from_student/', AnswerFromStudentPostAPIView.as_view()),
]
from django.urls import path
from .views import CategoryListAPIView, QuestionListAPIView, ResultListAPIView, \
    AnswerFromStudentPostAPIView, AverageStatisticByCategoryListAPIView


urlpatterns = [
    path('category/', CategoryListAPIView.as_view()),
    path('category/<int:category_id>/question/', QuestionListAPIView.as_view()),
    path('result/', ResultListAPIView.as_view()),
    path('answer_from_student/', AnswerFromStudentPostAPIView.as_view()),
    path('average_by_category/', AverageStatisticByCategoryListAPIView.as_view()),
]
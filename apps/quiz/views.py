from django.http import HttpResponseNotFound
from rest_framework import generics
from .models import Category, Question, Option, Result
from .serializers import CategorySerializer, QuestionSerializer, ResultSerializer


class CategoryListAPIView(generics.ListAPIView):  # category list
    # http://127.0.0.1:8000/quiz/
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class QuestionListAPIView(generics.ListAPIView):  # quesiton list with filtered options
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.kwargs['category_id']
        if category_id:
            qs = qs.filter(category_id=category_id)
            return qs
        return HttpResponseNotFound('Not found!')


class ResultListAPIView(generics.ListAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
from django.http import HttpResponseNotFound
from rest_framework import generics
from rest_framework.views import APIView
from .models import Category, Question, Option, Result
from .serializers import CategorySerializer, QuestionSerializer, ResultSerializer
from rest_framework.response import Response


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


class AnswerFromStudentPostAPIView(APIView):
    def post(self, request):
        global option_from_model
        account = self.request.user
        category_id = int(self.request.data.get('category_id'))
        question_id = int(self.request.data.get('question_id'))
        option_id = int(self.request.data.get('option_id'))
        # to check answer
        options = Option.objects.all()
        for option in options:
            if option_id == option.id:
                option_from_model = option
        if question_id:
            if option_from_model.is_correct:
                pass
                return Response("Correct")
        return Response("Incorrect")
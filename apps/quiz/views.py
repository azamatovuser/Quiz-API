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
        count = 0
        account = self.request.user
        category_id = self.request.data.get('category_id')
        questions = self.request.data.get('questions')
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response("Category not found")
        result = Result.objects.create(account_id=account.id, category_id=category_id)
        for i in questions:
            question_id = int(i.get('question_id'))
            option_id = int(i.get('option_id'))
            try:
                question = Question.objects.get(id=question_id)
                option = Option.objects.get(id=option_id)
            except (Question.DoesNotExist, Option.DoesNotExist):
                continue
            if option.is_correct:
                count += 20
            result.questions.add(question)
        result.result = count
        result.save()
        return Response("Result was saved")
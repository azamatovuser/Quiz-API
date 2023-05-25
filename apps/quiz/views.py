from django.http import HttpResponseNotFound
from rest_framework import generics
from rest_framework.views import APIView
from .models import Category, Question, Option, Result
from .serializers import CategorySerializer, QuestionSerializer, ResultSerializer
from rest_framework.response import Response
from operator import attrgetter
from apps.account.models import Account
from apps.account.serializers import AccountSerializer
from django.db.models import Q
from django.utils import timezone
from django.db.models import Count
from datetime import datetime, timedelta
from django.db.models.functions import TruncWeek, TruncDay, TruncMonth


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

    def get_queryset(self):
        qs = super().get_queryset()
        qs = sorted(qs, key=attrgetter('result'), reverse=True)
        return qs


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

    # Example of sending data
    # {
    #   "category_id": 1,
    #   "questions": [
    #     {
    #       "question_id": 1,
    #       "option_id": 3
    #     },
    #     {
    #       "question_id": 2,
    #       "option_id": 1
    #     },
    #     ...
    #   ]
    # }


class AverageStatisticByCategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        category_results = []
        for category in categories:
            average_result = Result.calculate_average_result(category)
            category_results.append({
                'title': category.title,
                'average_result': average_result
            })
        return Response(category_results)


class AverageStatisticByAccountListAPIView(APIView):
    def get(self, request):
        accounts = Account.objects.all()
        account_results = []
        for account in accounts:
            average_result_account = Result.calculate_average_result_account(account)
            serialized_account = AccountSerializer(account).data
            account_results.append({
                "account": serialized_account,
                "average_result_account": average_result_account
            })
        return Response(account_results)


class DayStatisticListAPIView(generics.ListAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    def get_queryset(self):
        qs = Result.objects.annotate(day=TruncDay('created_date')).filter(day=timezone.now().date()).annotate(total_results=Count('id'))
        return qs


class WeekStatisticListAPIView(generics.ListAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    def get_queryset(self):
        now = timezone.now().date()
        past_week = now - timedelta(days=7)
        qs = Result.objects.filter(created_date__range=[past_week, now]).annotate(total_results=Count('id'))
        return qs


class MonthStatisticListAPIView(generics.ListAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    def get_queryset(self):
        now = timezone.now().date()
        past_month = now - timedelta(days=30)
        qs = Result.objects.filter(created_date__range=[past_month, now]).annotate(total_results=Count('id'))
        return qs
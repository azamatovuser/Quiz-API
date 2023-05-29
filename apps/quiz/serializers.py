from rest_framework import serializers
from .models import Question, Option, Result, Category, Contact


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'question', 'option', 'is_correct']


class OptionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option']


class QuestionSerializer(serializers.ModelSerializer):
    option = OptionSerializer(read_only=True, many=True)
    class Meta:
        model = Question
        fields = ['id', 'category', 'question', 'option']


class QuestionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'category', 'question']


class QuestionOptionSerializer(serializers.ModelSerializer):
    option = OptionResultSerializer(many=True)
    class Meta:
        model = Question
        fields = ['id', 'category', 'question', 'option']


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id', 'account', 'category', 'questions', 'result']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
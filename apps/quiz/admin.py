from django.contrib import admin
from .models import Category, Question, Option, Result


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class OptionInlineAdmin(admin.TabularInline):
    model = Option
    readonly_fields = ('id', )
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInlineAdmin]
    list_display = ('id', 'category', 'question')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'category', 'get_questions', 'result')

    def get_questions(self, obj):
        return ", ".join([question.question for question in obj.questions.all()])
from django.db import models, IntegrityError
from apps.account.models import Account
from django.db.models import Avg
from django.db.models import Q, UniqueConstraint


class TimeStamp(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Category(TimeStamp):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class Question(TimeStamp):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.CharField(max_length=221)

    @classmethod
    def filter_new_questions(cls, account):
        old_questions = Result.objects.filter(account=account).values('questions')
        new_questions = cls.objects.exclude(id__in=old_questions)
        return new_questions


    def __str__(self):
        return f"{self.category}'s question: {self.question}"


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='option')
    option = models.CharField(max_length=221)
    is_correct = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['question'],
                condition=Q(is_correct=True),
                name='unique_correct_option'
            )
        ]

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except:
            raise IntegrityError('Only one option can be marked as correct for a question.')

    def __str__(self):
        return f"{self.question}'s answers"


class Result(TimeStamp):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, null=True, blank=True)
    result = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.account}'s result is - {self.result} in {self.category}"

    @classmethod
    def calculate_average_result(cls, category):
        average_result = cls.objects.filter(category=category).aggregate(Avg('result'))['result__avg']
        return average_result

    @classmethod
    def calculate_average_result_account(cls, account):
        average_result = cls.objects.filter(account=account).aggregate(Avg('result'))['result__avg']
        return average_result


class Contact(TimeStamp):
    name = models.CharField(max_length=221)
    email = models.EmailField(unique=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.name}'s message"
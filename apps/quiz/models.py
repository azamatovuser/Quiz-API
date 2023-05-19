from django.db import models
from apps.account.models import Account


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

    def __str__(self):
        return f"{self.category}'s question: {self.question}"


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='option')
    option = models.CharField(max_length=221)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question}'s answers"


class Result(TimeStamp):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    result = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.account}'s result is - {self.result} in {self.category}"
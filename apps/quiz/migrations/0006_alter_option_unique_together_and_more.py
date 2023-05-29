# Generated by Django 4.2.1 on 2023-05-29 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_alter_option_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='option',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='option',
            constraint=models.UniqueConstraint(condition=models.Q(('is_correct', True)), fields=('question',), name='unique_correct_option'),
        ),
    ]
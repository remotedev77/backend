# Generated by Django 4.2.6 on 2023-11-09 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_alter_question_correct_answer_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='note',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='question_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='work_function',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
# Generated by Django 4.2.6 on 2023-11-28 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complianceanswer',
            old_name='qestion_id',
            new_name='question_id',
        ),
    ]
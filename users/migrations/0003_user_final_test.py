# Generated by Django 4.1.7 on 2023-10-28 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='final_test',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]

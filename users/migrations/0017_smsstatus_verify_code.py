# Generated by Django 4.2.6 on 2024-03-25 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_smsstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsstatus',
            name='verify_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

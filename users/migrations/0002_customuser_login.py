# Generated by Django 4.2.20 on 2025-05-10 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='login',
            field=models.CharField(blank=True, null=True, unique=True),
        ),
    ]

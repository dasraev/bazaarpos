# Generated by Django 4.2.20 on 2025-05-06 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='stores/'),
        ),
        migrations.AddField(
            model_name='store',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]

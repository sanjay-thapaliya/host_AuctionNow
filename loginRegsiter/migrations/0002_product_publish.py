# Generated by Django 3.1.3 on 2020-12-05 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginRegsiter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='publish',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 2.1 on 2018-08-24 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_phone',
            field=models.CharField(max_length=15),
        ),
    ]
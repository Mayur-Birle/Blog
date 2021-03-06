# Generated by Django 2.1 on 2018-09-08 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0004_auto_20180824_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.BooleanField(default=False)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.Posts')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.Users')),
            ],
        ),
    ]

# Generated by Django 4.2.5 on 2023-10-05 19:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrot_app', '0007_chatroom_remove_userprofile_user_certification_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mannertemperature',
            name='last_vote_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('남', '남자'), ('여', '여자'), ('O', '설정 않음')], max_length=1, null=True),
        ),
    ]
# Generated by Django 2.0.6 on 2018-08-08 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports50web', '0003_auto_20180807_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='players',
            name='draft_number',
            field=models.IntegerField(null=True),
        ),
    ]
# Generated by Django 2.0.6 on 2019-06-06 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports50web', '0010_auto_20190606_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stadiums',
            name='super_bowl_year',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

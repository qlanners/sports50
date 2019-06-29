# Generated by Django 2.0.6 on 2019-06-06 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sports50web', '0007_auto_20180922_1928'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stadiums',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stadium_name', models.CharField(max_length=50, null=True)),
                ('stadium_lat', models.DecimalField(decimal_places=4, max_digits=8, null=True)),
                ('stadium_lon', models.DecimalField(decimal_places=4, max_digits=8, null=True)),
                ('state', models.CharField(max_length=50, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('country', models.CharField(max_length=50, null=True)),
                ('years', models.TextField(null=True)),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports50web.Sports')),
            ],
        ),
        migrations.RemoveField(
            model_name='teams',
            name='city',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='country',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='home_stadium_lat',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='home_stadium_lon',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='home_stadium_name',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='state',
        ),
        migrations.AddField(
            model_name='stadiums',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports50web.Teams'),
        ),
    ]

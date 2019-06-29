# Generated by Django 2.0.6 on 2018-08-07 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sports50web', '0002_teams'),
    ]

    operations = [
        migrations.CreateModel(
            name='Football_Passing_Plays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarter', models.IntegerField()),
                ('time', models.TimeField()),
                ('down', models.IntegerField()),
                ('to_go', models.IntegerField()),
                ('side_of_field', models.IntegerField(choices=[(0, '50 yeard line'), (1, 'own side of field'), (2, 'opponent side of field')])),
                ('yard_line', models.IntegerField()),
                ('team_points', models.IntegerField()),
                ('opponent_points', models.IntegerField()),
                ('description', models.CharField(max_length=500, null=True)),
                ('yards', models.IntegerField()),
                ('epb', models.DecimalField(decimal_places=4, max_digits=8, null=True)),
                ('epa', models.DecimalField(decimal_places=4, max_digits=8, null=True)),
                ('diff', models.DecimalField(decimal_places=4, max_digits=8, null=True)),
                ('incomplete', models.IntegerField()),
                ('complete', models.IntegerField()),
                ('touchdown', models.IntegerField()),
                ('interception', models.IntegerField()),
                ('pick_six', models.IntegerField()),
                ('sack', models.IntegerField()),
                ('spike', models.IntegerField()),
                ('penalty', models.IntegerField()),
                ('declined', models.IntegerField()),
                ('fumble', models.IntegerField()),
                ('short', models.IntegerField()),
                ('deep', models.IntegerField()),
                ('left', models.IntegerField()),
                ('right', models.IntegerField()),
                ('middle', models.IntegerField()),
                ('no_play', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GameLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('season', models.IntegerField(null=True)),
                ('week', models.IntegerField(null=True)),
                ('day', models.CharField(choices=[('Sun', 'Sunday'), ('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday')], max_length=3, null=True)),
                ('time', models.CharField(max_length=20, null=True)),
                ('home_field_team', models.IntegerField(choices=[(1, 'Team One Home'), (2, 'Team Two Home'), (0, 'Neutral Location')], default=3)),
                ('result', models.IntegerField(choices=[(1, 'Team One Wins'), (2, 'Team Two Wins'), (0, 'Tie')])),
                ('team_one_points', models.IntegerField()),
                ('team_two_points', models.IntegerField()),
                ('team_one_yards', models.IntegerField()),
                ('team_two_yards', models.IntegerField()),
                ('team_one_turnovers', models.IntegerField()),
                ('team_two_turnovers', models.IntegerField()),
                ('sport_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports50web.Sports')),
                ('team_one_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_one', to='sports50web.Teams')),
                ('team_two_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_two', to='sports50web.Teams')),
            ],
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.CharField(max_length=20, null=True)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('dob', models.DateTimeField(null=True)),
                ('home_country', models.CharField(max_length=50, null=True)),
                ('home_state', models.CharField(max_length=50, null=True)),
                ('home_city', models.CharField(max_length=50, null=True)),
                ('high_school', models.CharField(max_length=50, null=True)),
                ('high_school_city', models.CharField(max_length=50, null=True)),
                ('high_school_state', models.CharField(max_length=50, null=True)),
                ('college', models.CharField(max_length=50, null=True)),
                ('college_city', models.CharField(max_length=50, null=True)),
                ('college_state', models.CharField(max_length=50, null=True)),
                ('draft_year', models.IntegerField(null=True)),
                ('draft_round', models.IntegerField(null=True)),
                ('debut', models.DateTimeField(null=True)),
                ('dominant_hand', models.CharField(choices=[('L', 'Left'), ('R', 'Right')], max_length=1, null=True)),
                ('bats', models.CharField(choices=[('L', 'Left'), ('R', 'Right'), ('S', 'Switch')], max_length=1, null=True)),
                ('height', models.IntegerField(null=True)),
                ('weight', models.IntegerField(null=True)),
                ('hall_of_fame', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_position', models.CharField(max_length=25)),
                ('abbrev_position', models.CharField(max_length=5)),
                ('sport_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports50web.Sports')),
            ],
        ),
        migrations.AddField(
            model_name='players',
            name='primary_position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sports50web.Positions'),
        ),
        migrations.AddField(
            model_name='football_passing_plays',
            name='game_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports50web.GameLog'),
        ),
        migrations.AddField(
            model_name='football_passing_plays',
            name='opponent_team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opponent', to='sports50web.Teams'),
        ),
        migrations.AddField(
            model_name='football_passing_plays',
            name='player_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports50web.Players'),
        ),
        migrations.AddField(
            model_name='football_passing_plays',
            name='sport_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports50web.Sports'),
        ),
        migrations.AddField(
            model_name='football_passing_plays',
            name='team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='sports50web.Teams'),
        ),
    ]

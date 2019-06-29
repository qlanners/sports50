from django.db import models
from decimal import Decimal


class Sports(models.Model):
	sport_name = models.CharField(max_length=50)

	def __str__(self):
		return self.sport_name


class Teams(models.Model):
	sport = models.ForeignKey(Sports, on_delete=models.CASCADE)
	LEVEL_CHOICES = [('I', 'International'),('P', 'Professional'),('S','Semi-Professional'),('C', 'College')]
	level = models.CharField(choices=LEVEL_CHOICES, max_length=1)	
	league = models.CharField(null=True, max_length=50)
	division = models.CharField(null=True, max_length=30)
	mascot = models.CharField(null=True, max_length=30)
	full_name = models.CharField(max_length=50)
	abbrev = models.CharField(max_length=5)
	first_year = models.IntegerField(null=True)
	titles = models.IntegerField()
	logo = models.CharField(max_length=500)

	def __str__(self):
		return self.full_name

class Stadiums(models.Model):
	sport = models.ForeignKey(Sports, on_delete=models.CASCADE)
	team = models.ForeignKey(Teams, on_delete=models.CASCADE)
	stadium_name = models.CharField(null=True, max_length=50)
	stadium_lat = models.DecimalField(null=True, max_digits=8, decimal_places=4)
	stadium_lon = models.DecimalField(null=True, max_digits=8, decimal_places=4)
	state = models.CharField(null=True, max_length=50)
	city = models.CharField(null=True, max_length=50)	
	country = models.CharField(null=True, max_length=50)
	first_year = models.IntegerField(null=True)
	last_year = models.IntegerField(default=2050)
	super_bowl = models.IntegerField(default=0)
	super_bowl_year = models.CharField(null=True, max_length=50)

	def __str__(self):
		return self.stadium_name


class Positions(models.Model):
	sport = models.ForeignKey(Sports, on_delete=models.CASCADE)
	full_position = models.CharField(max_length=25)
	abbrev_position = models.CharField(max_length=5)

	def __str__(self):
		return self.abbrev_position

class Players(models.Model):
	DOMINANT_HAND_CHOICES = [('L', 'Left'),('R', 'Right')]
	BATS_CHOICES = [('L', 'Left'),('R', 'Right'),('S', 'Switch')]
	reference_id = models.CharField(max_length=20, null=True)	
	first_name = models.CharField(max_length=30, null=True)
	last_name = models.CharField(max_length=30, null=True)
	primary_position = models.ForeignKey(Positions, on_delete=models.CASCADE, null=True)
	dob = models.DateTimeField(null=True)
	home_country = models.CharField(max_length=50, null=True)
	home_state = models.CharField(null=True, max_length=50)
	home_city = models.CharField(null=True, max_length=50)
	high_school = models.CharField(max_length=50, null=True)
	high_school_city = models.CharField(null=True, max_length=50)
	high_school_state = models.CharField(null=True, max_length=50)
	college = models.CharField(max_length=50, null=True)
	college_city = models.CharField(null=True, max_length=50)
	college_state = models.CharField(null=True, max_length=50)
	draft_year = models.IntegerField(null=True)
	draft_round = models.IntegerField(null=True)
	draft_number = models.IntegerField(null=True)
	debut = models.DateTimeField(null=True)
	dominant_hand = models.CharField(choices=DOMINANT_HAND_CHOICES, max_length=1, null=True)
	bats = models.CharField(choices=BATS_CHOICES, max_length=1, null=True)
	height = models.IntegerField(null=True)
	weight = models.IntegerField(null=True)
	hall_of_fame = models.IntegerField(null=True)

	def __str__(self):
		return self.first_name + ' ' + self.last_name


class GameLog(models.Model):
	HOME_FIELD_TEAM_COICES = [(1, 'Team One Home'),(2, 'Team Two Home'),(0, 'Neutral Location')]
	RESULT_COICES = [(1, 'Team One Wins'),(2, 'Team Two Wins'),(0, 'Tie')]
	DAY_CHOICES = [('Sun', 'Sunday'),('Mon', 'Monday'),('Tue', 'Tuesday'),('Wed', 'Wednesday'),('Thu', 'Thursday'),('Fri', 'Friday'),('Sat', 'Saturday')]
	sport = models.ForeignKey(Sports, on_delete=models.CASCADE)
	date = models.DateTimeField()
	season = models.IntegerField(null=True)
	week = models.IntegerField(null=True)
	day = models.CharField(choices=DAY_CHOICES, max_length=3, null=True)
	time = models.CharField(max_length=20, null=True)
	team_one = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='team_one')
	team_two = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='team_two')
	home_field_team = models.IntegerField(choices=HOME_FIELD_TEAM_COICES, default=3)
	result = models.IntegerField(choices=RESULT_COICES)
	team_one_points = models.IntegerField()
	team_two_points = models.IntegerField()
	team_one_yards = models.IntegerField()
	team_two_yards = models.IntegerField()
	team_one_turnovers = models.IntegerField()
	team_two_turnovers = models.IntegerField()

	def __str__(self):
		return str(self.season) + ' week ' + str(self.week) + ': ' + self.team_one.abbrev + ' vs. ' + self.team_two.abbrev

class Football_Passing_Plays(models.Model):
	SIDE_OF_FIELD_CHOICES = [(0,'50 yeard line'),(1,'own side of field'),(2,'opponent side of field')]
	sport = models.ForeignKey(Sports, on_delete=models.CASCADE)
	team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='team')
	opponent_team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='opponent')
	player = models.ForeignKey(Players, on_delete=models.CASCADE)
	game = models.ForeignKey(GameLog, on_delete=models.CASCADE)
	quarter = models.IntegerField()
	time = models.TimeField()
	down = models.IntegerField()
	to_go = models.IntegerField()
	side_of_field = models.IntegerField(choices=SIDE_OF_FIELD_CHOICES)
	yard_line = models.IntegerField()
	team_points = models.IntegerField()
	opponent_points = models.IntegerField()
	description = models.CharField(max_length=1000, null=True)
	yards = models.IntegerField()
	epb = models.DecimalField(null=True, max_digits=8, decimal_places=4)
	epa = models.DecimalField(null=True, max_digits=8, decimal_places=4)
	diff = models.DecimalField(null=True, max_digits=8, decimal_places=4)
	incomplete = models.IntegerField()
	complete = models.IntegerField()
	touchdown = models.IntegerField()
	interception = models.IntegerField()
	pick_six = models.IntegerField()
	sack = models.IntegerField()
	spike = models.IntegerField()
	penalty = models.IntegerField()
	declined = models.IntegerField()
	fumble = models.IntegerField()
	short = models.IntegerField()
	deep = models.IntegerField()
	left = models.IntegerField()
	right = models.IntegerField()
	middle = models.IntegerField()
	no_play = models.IntegerField()
	
	def __str__(self):
		if self.complete == 1:
			return self.player.first_name + ' ' + self.player.last_name + ' complete for ' + str(self.yards) + ' yards'
		else:
			return self.player.first_name + ' ' + self.player.last_name + ' incomplete'

class Football_Rushing_Plays(models.Model):
	SIDE_OF_FIELD_CHOICES = [(0,'50 yeard line'),(1,'own side of field'),(2,'opponent side of field')]
	sport = models.ForeignKey(Sports, on_delete=models.CASCADE)
	team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='team_rushing')
	opponent_team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='opponent_rushing')
	player = models.ForeignKey(Players, on_delete=models.CASCADE)
	game = models.ForeignKey(GameLog, on_delete=models.CASCADE)
	quarter = models.IntegerField()
	time = models.TimeField()
	down = models.IntegerField()
	to_go = models.IntegerField()
	side_of_field = models.IntegerField(choices=SIDE_OF_FIELD_CHOICES)
	yard_line = models.IntegerField()
	team_points = models.IntegerField()
	opponent_points = models.IntegerField()
	description = models.CharField(max_length=1000, null=True)
	yards = models.IntegerField()
	epb = models.DecimalField(null=True, max_digits=8, decimal_places=4)
	epa = models.DecimalField(null=True, max_digits=8, decimal_places=4)
	diff = models.DecimalField(null=True, max_digits=8, decimal_places=4)
	touchdown = models.IntegerField()
	penalty = models.IntegerField()
	declined = models.IntegerField()
	fumble = models.IntegerField()
	tackle_for_loss = models.IntegerField()
	tackle = models.IntegerField()
	guard = models.IntegerField()
	end = models.IntegerField()
	left = models.IntegerField()
	right = models.IntegerField()
	middle = models.IntegerField()
	no_play = models.IntegerField()
	
	def __str__(self):
		return self.player.first_name + ' ' + self.player.last_name + ' rush for ' + str(self.yards) + ' yards'


'''
class TeamList(models.Model):
	team_id = models.ForeignKey(Teams, on_delete=models.CASCADE)
	player_id = models.ForeignKey(Players, on_delete=models.CASCADE)

class Baseball_Batting_Stats(models.Model):
	sport_id = models.ForeignKey(Sports, on_delete=models.CASCADE)
	team_id = models.ForeignKey(Teams, on_delete=models.CASCADE)
	player_id = models.ForeignKey(Players, on_delete=models.CASCADE)
	game_id = models.ForeignKey(GameLog, on_delete=models.CASCADE)
	career_game_number = models.IntegerField(null=True)
	season_game_number = models.IntegerField(null=True)
	games_missed_this_season_to_date = models.IntegerField(null=True)
	innings_played = models.IntegerField(null=True)
	plate_appearances = models.IntegerField(null=True)
	at_bats = models.IntegerField(null=True)
	runs_scored = models.IntegerField(null=True)
	hits = models.IntegerField(null=True)
	doubles = models.IntegerField(null=True)
	triples = models.IntegerField(null=True)
	home_runs = models.IntegerField(null=True)
	runs_batted_in = models.IntegerField(null=True)
	walks = models.IntegerField(null=True)
	intentional_walks = models.IntegerField(null=True)
	strike_outs = models.IntegerField(null=True)
	hit_by_pitch = models.IntegerField(null=True)
	sacrifice_hits = models.IntegerField(null=True)
	sacrifice_flies = models.IntegerField(null=True)
	reached_on_error = models.IntegerField(null=True)
	doubles_plays_grounded_into = models.IntegerField(null=True)
	stolen_bases = models.IntegerField(null=True)
	caught_stealing = models.IntegerField(null=True)
	batting_average = models.DecimalField(decimal_places=3, null=True)
	on_base_percentage = models.DecimalField(decimal_places=3, null=True)
	slugging_percentage = models.DecimalField(decimal_places=3, null=True)
	ops = models.DecimalField(decimal_places=3, null=True)
	batting_order_position = models.IntegerField()
	average_leverage_index = models.DecimalField(decimal_places=2, null=True)
	wpa = models.DecimalField(decimal_places=3, null=True)
	re24 = models.DecimalField(decimal_places=3, null=True)
	fantasy_points_drafts_kings = models.DecimalField(decimal_places=3, null=True)
	fantasy_points_fan_duel = models.DecimalField(decimal_places=3, null=True)

class Baseball_Pitching_Stats(models.Model):
	sport_id = models.ForeignKey(Sports, on_delete=models.CASCADE)
	team_id = models.ForeignKey(Teams, on_delete=models.CASCADE)
	player_id = models.ForeignKey(Players, on_delete=models.CASCADE)
	game_id = models.ForeignKey(GameLog, on_delete=models.CASCADE)
	decision = models.CharField(null=True, max_length=3)
	days_rest = models.IntegerField(null=True)
	innings_pitched = models.DecimalField(decimal_places=1,null=True)
	hits_allowed = models.IntegerField(null=True)
	runs_allowed = models.IntegerField(null=True)
	earned_runs = models.IntegerField(null=True)
	walks = models.IntegerField(null=True)
	strike_outs = models.IntegerField(null=True)
	home_runs_allowed = models.IntegerField(null=True)
	hit_batter = models.IntegerField(null=True)
	era = models.IntegerField(null=True, decimal_places=2)
	batters_faced = models.IntegerField(null=True)
	ground_balls = models.IntegerField(null=True)
	fly_balls = models.IntegerField(null=True)
	line_drives = models.IntegerField(null=True)
	pop_ups = models.IntegerField(null=True)
	unknown_batted_ball_type = models.IntegerField(null=True)
	game_score = models.IntegerField(null=True)
	inherited_runners = models.IntegerField(null=True)
	inherited_score = models.IntegerField(null=True)
	stolen_bases = models.IntegerField(null=True)
	caught_stealing = models.IntegerField(null=True)
	pick_offs = models.IntegerField(null=True)
	at_bats = models.IntegerField(null=True)
	doubles_allowed = models.IntegerField(null=True)
	triples_allowed = models.IntegerField(null=True)
	intentional_walks = models.IntegerField(null=True)
	doubles_plays_grounded_into = models.IntegerField(null=True)
	sacrifice_flies = models.IntegerField(null=True)
	reached_on_error = models.IntegerField(null=True)
	average_leverage_index = models.DecimalField(decimal_places=2, null=True)
	win_prob_added = models.DecimalField(decimal_places=3, null=True)
	base_out_runs_saved = models.DecimalField(decimal_places=2, null=True)
	inning_entered = models.IntegerField(null=True)
	inning_exited = models.IntegerField(null=True)
	


class Baseball_Fielding_Stats(models.Model):
	sport_id = models.ForeignKey(Sports, on_delete=models.CASCADE)
	team_id = models.ForeignKey(Teams, on_delete=models.CASCADE)
	player_id = models.ForeignKey(Players, on_delete=models.CASCADE)
	game_id = models.ForeignKey(GameLog, on_delete=models.CASCADE)
	batters_faced = models.IntegerField(null=True)
	innings = models.IntegerField(null=True)
	putouts = models.IntegerField(null=True)
	assists = models.IntegerField(null=True)
	errors = models.IntegerField(null=True)
	chances = models.IntegerField(null=True)
	double_plays_turned = models.IntegerField(null=True)
	position = models.ForeignKey(Positions, on_delete=models.CASCADE)


class Positions(models.Model):
	sport_id = models.ForeignKey(Sports, on_delete=models.CASCADE)
	position = models.CharField(max_length=50)

'''
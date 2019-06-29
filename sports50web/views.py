from django.http import HttpResponse
from django.views.generic import FormView 
from django.db.models import F, Q
from django.db.models import Sum
from django.db.models import Avg
from django.db.models import Count
from django.shortcuts import render, render_to_response
from django.db.models import Case, CharField, Value, When
import json
import itertools

from bokeh.plotting import figure, output_file, show 
from bokeh.embed import components

from .models import Teams
from .models import GameLog
from .models import Players
from .models import Football_Passing_Plays
from .models import Stadiums
from .models import Football_Rushing_Plays

import simplejson
from operator import truediv
from operator import add


years = [2010,2011,2012,2013,2014,2015,2016,2017]

def home(request):
	teams = Teams.objects.filter(sport=2).order_by('full_name')			

	return render_to_response('home.html', {'teams':teams})

def team_info(request, team_id):
	teams = Teams.objects.filter(sport=2).order_by('full_name')
	this_team = Teams.objects.filter(id=team_id)
	this_team_logo = list(this_team.values_list('logo'))[0]

	return render_to_response('team_info.html', {'teams': teams, 'this_team': this_team, 'team_logo': json.dumps(this_team_logo)})	




def field_breakdown(request, team_id):
	# my_filter = {}
	# if int(team_id)!=0:
	# 	my_filter['team'] = team_id
	# location_td = location_td_filter_passing(my_filter)
	print(team_id)
	if int(team_id) == 0:
		this_team_logo = ["https://www.stickpng.com/assets/images/5895deb9cba9841eabab6099.png"]
	else:
		this_team = Teams.objects.filter(id=team_id)
		this_team_logo = list(this_team.values_list('logo'))[0]

	return render_to_response('field_breakdown.html', {'team_id': team_id, 'team_logo': json.dumps(this_team_logo)})

def field_breakdown_passing(request, team_id):
	my_filter = {}
	if int(team_id)!=0:
		my_filter['team'] = team_id
	location_td = location_td_filter_passing(my_filter)

	return render_to_response('field_breakdown_passing.html', {'location_td':json.dumps(location_td)})	

def field_breakdown_rushing(request, team_id):
	my_filter = {}
	if int(team_id)!=0:
		my_filter['team'] = team_id
	location_td = location_td_filter_rushing(my_filter)

	return render_to_response('field_breakdown_rushing.html', {'location_td':json.dumps(location_td)})


def stadium_map(request, team_id):

	return render_to_response('stadium_map.html', {'team_id': team_id})

def stadium_map_passing(request, team_id):
	my_filter = {}
	if int(team_id)!=0:
		my_filter['team'] = team_id
	stadiums = stadium_map_filter_passing(my_filter)

	return render_to_response('stadium_map_passing.html', {'stadiums':simplejson.dumps(stadiums, use_decimal=True)})

def stadium_map_rushing(request, team_id):
	my_filter = {}
	if int(team_id)!=0:
		my_filter['team'] = team_id
	stadiums = stadium_map_filter_rushing(my_filter)

	return render_to_response('stadium_map_rushing.html', {'stadiums':simplejson.dumps(stadiums, use_decimal=True)})	

def passing_zones(request, team_id):
	my_filter = {}
	if int(team_id)!=0:
		my_filter['team'] = team_id
	passing_zones_complete, passing_zones_incomplete = passing_zones_filter(my_filter)

	return render_to_response('passing_zones.html', {'passing_zones_complete':json.dumps(passing_zones_complete), 'passing_zones_incomplete':json.dumps(passing_zones_incomplete)})	



def location_td_filter_passing(my_filter):
	location_td = {
		'touchdown__sum': {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]}, 'interception__sum': {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]},
		'pick_six__sum': {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]}, 'fumble__sum': {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]},
		'sack__sum': {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]}, 'penalty__sum': {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]},
		'complete__sum': {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]}, 'incomplete__sum': {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]},
		'percentage__sum': {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]}}
	combos = [(1,1,10),(1,11,20),(1,21,30),(1,31,40),(1,41,50),(2,41,49),(2,31,40),(2,21,30),(2,11,20),(2,1,10)]
	for combo in combos:
		for season in list(Football_Passing_Plays.objects.values('game__season').filter(**my_filter).filter(side_of_field=combo[0]).filter(yard_line__gte=combo[1], yard_line__lte=combo[2]).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('fumble')).annotate(Sum('sack')).annotate(Sum('penalty')).annotate(Sum('complete')).annotate(Sum('incomplete'))):
			for key, value in location_td.items():
				if key != 'percentage__sum':
					for k, v in value.items():
						if k == season['game__season']:
							location_td[key][k].append(season[key])
		if combo[2] == 50:
			for season in list(Football_Passing_Plays.objects.values('game__season').filter(**my_filter).filter(side_of_field=0).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('fumble')).annotate(Sum('sack')).annotate(Sum('penalty')).annotate(Sum('complete')).annotate(Sum('incomplete'))):
				for key, value in location_td.items():
					if key != 'percentage__sum':
						for k, v in value.items():
							if k == season['game__season']:
								location_td[key][k][-1] = location_td[key][k][-1] + season[key]
	for k,v in location_td['complete__sum'].items():
		location_td['percentage__sum'][k] = list(map(truediv,v,list(map(add,v,location_td['incomplete__sum'][k]))))	

	return location_td	

def location_td_filter_rushing(my_filter):
	location_td = {
		'touchdown__sum': {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]}, 'tackle_for_loss__sum': {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]},
		'fumble__sum': {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]}, 'penalty__sum': {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]}}
	combos = [(1,1,10),(1,11,20),(1,21,30),(1,31,40),(1,41,50),(2,41,49),(2,31,40),(2,21,30),(2,11,20),(2,1,10)]
	for combo in combos:
		for season in list(Football_Rushing_Plays.objects.values('game__season').filter(**my_filter).filter(side_of_field=combo[0]).filter(yard_line__gte=combo[1], yard_line__lte=combo[2]).annotate(Sum('touchdown')).annotate(Sum('fumble')).annotate(Sum('penalty')).annotate(Sum('tackle_for_loss'))):
			for key, value in location_td.items():
				if key != 'percentage__sum':
					for k, v in value.items():
						if k == season['game__season']:
							location_td[key][k].append(season[key])
		if combo[2] == 50:
			for season in list(Football_Rushing_Plays.objects.values('game__season').filter(**my_filter).filter(side_of_field=0).annotate(Sum('touchdown')).annotate(Sum('fumble')).annotate(Sum('penalty')).annotate(Sum('tackle_for_loss'))):
				for key, value in location_td.items():
					if key != 'percentage__sum':
						for k, v in value.items():
							if k == season['game__season']:
								location_td[key][k][-1] = location_td[key][k][-1] + season[key]

	return location_td		


def stadium_map_filter_passing(my_filter):
	stadiums = []

	stadiums_db = Stadiums.objects.filter(sport=2).filter(last_year__gte=2010).order_by('team_id')

	blank_year = {'touchdown__sum':0, 'interception__sum':0, 'pick_six__sum':0, 'fumble__sum':0, 'sack__sum':0, 'penalty__sum':0, 'complete__sum':0, 'incomplete__sum': 0}

	stads_done = []
	for stad in stadiums_db:
		stat_per_stad = {
	'touchdown__sum': {2010:0,2011:0,2012:0,2013:0,2014:0,2015:0,2016:0,2017:0}, 'interception__sum': {2010:0,2011:0,2012:0,2013:0,2014:0,2015:0,2016:0,2017:0},
	'pick_six__sum': {2010:0,2011:0,2012:0,2013:0,2014:0,2015:0,2016:0,2017:0}, 'fumble__sum': {2010:0,2011:0,2012:0,2013:0,2014:0,2015:0,2016:0,2017:0},
	'sack__sum': {2010:0,2011:0,2012:0,2013:0,2014:0,2015:0,2016:0,2017:0}, 'penalty__sum': {2010:0,2011:0,2012:0,2013:0,2014:0,2015:0,2016:0,2017:0},
	'complete__sum': {2010:0,2011:0,2012:0,2013:0,2014:0,2015:0,2016:0,2017:0}, 'incomplete__sum': {2010:0,2011:0,2012:0,2013:0,2014:0,2015:0,2016:0,2017:0},
	'percentage__sum': {2010:0,2011:0,2012:0,2013:0,2014:0,2015:0,2016:0,2017:0}}
		l1 = Football_Passing_Plays.objects.values('game__season').filter(**my_filter).filter(game__home_field_team=1).filter(game__team_one=stad.team.id).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('fumble')).annotate(Sum('sack')).annotate(Sum('penalty')).annotate(Sum('complete')).annotate(Sum('incomplete'))
		l2 = Football_Passing_Plays.objects.values('game__season').filter(**my_filter).filter(game__home_field_team=2).filter(game__team_two=stad.team.id).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('fumble')).annotate(Sum('sack')).annotate(Sum('penalty')).annotate(Sum('complete')).annotate(Sum('incomplete'))
		if stad.stadium_name not in stads_done:
			if stad.first_year <= 2010:
				for i in range(2010,stad.last_year+1 if stad.last_year+1<=2018 else 2018):
					e = stad.stadium_name
					year1 = list(l1.filter(game__season=i))[0] if l1.filter(game__season=i) else blank_year
					year2 = list(l2.filter(game__season=i))[0] if l2.filter(game__season=i) else blank_year
					for k, v in stat_per_stad.items():
						if k != 'percentage__sum':
							stat_per_stad[k][i] += year1[k] +year2[k]
			else:
				for i in range(stad.first_year,stad.last_year+1 if stad.last_year+1<=2018 else 2018):
					e = stad.stadium_name
					year1 = list(l1.filter(game__season=i))[0] if l1.filter(game__season=i) else blank_year
					year2 = list(l2.filter(game__season=i))[0] if l2.filter(game__season=i) else blank_year
					for k, v in stat_per_stad.items():
						if k != 'percentage__sum':
							stat_per_stad[k][i] += year1[k] +year2[k]

			for k,v in stat_per_stad['complete__sum'].items():
				if (v+stat_per_stad['incomplete__sum'][k]) != 0:
					stat_per_stad['percentage__sum'][k] = v / (v+stat_per_stad['incomplete__sum'][k])
					


			stadiums.append([stad.state, stad.city, stad.stadium_name, stad.stadium_lon, stad.stadium_lat, stad.super_bowl, stat_per_stad])
			stads_done.append(stad.stadium_name)
		else:
			if stad.first_year <= 2010:
				for i in range(2010,stad.last_year+1 if stad.last_year+1<=2018 else 2018):
					year1 = list(l1.filter(game__season=i))[0] if l1.filter(game__season=i) else blank_year
					year2 = list(l2.filter(game__season=i))[0] if l2.filter(game__season=i) else blank_year
					for k, v in stat_per_stad.items():
						if k != 'percentage__sum':			
							stadiums[stads_done.index(stad.stadium_name)][6][k][i] += year1[k] +year2[k]
			else:
				for i in range(stad.first_year,stad.last_year+1 if stad.last_year+1<=2018 else 2018):
					year1 = list(l1.filter(game__season=i))[0] if l1.filter(game__season=i) else blank_year
					year2 = list(l2.filter(game__season=i))[0] if l2.filter(game__season=i) else blank_year
					for k, v in stat_per_stad.items():						
						if k != 'percentage__sum':
							stadiums[stads_done.index(stad.stadium_name)][6][k][i] += year1[k] +year2[k]
			for k,v in stat_per_stad['complete__sum'].items():
				if (v+stat_per_stad['incomplete__sum'][k]) != 0:
					stat_per_stad['percentage__sum'][k] = v / (v+stat_per_stad['incomplete__sum'][k])		

	return stadiums

def stadium_map_filter_rushing(my_filter):
	stadiums = []

	stadiums_db = Stadiums.objects.filter(sport=2).filter(last_year__gte=2010).order_by('team_id')

	blank_year = {'touchdown__sum':0, 'tackle_for_loss__sum':0, 'fumble__sum':0, 'penalty__sum':0}

	stads_done = []
	for stad in stadiums_db:
		stat_per_stad = {
	'touchdown__sum': {2010:0,2011:0,2012:0,2013:0,2014:0,2015:0,2016:0,2017:0}, 'tackle_for_loss__sum': {2010:0,2011:0,2012:0,2013:0,2014:0,2015:0,2016:0,2017:0},
	'fumble__sum': {2010:0,2011:0,2012:0,2013:0,2014:0,2015:0,2016:0,2017:0}, 'penalty__sum': {2010:0,2011:0,2012:0,2013:0,2014:0,2015:0,2016:0,2017:0}}
		l1 = Football_Rushing_Plays.objects.values('game__season').filter(**my_filter).filter(game__home_field_team=1).filter(game__team_one=stad.team.id).annotate(Sum('touchdown')).annotate(Sum('tackle_for_loss')).annotate(Sum('fumble')).annotate(Sum('penalty'))
		l2 = Football_Rushing_Plays.objects.values('game__season').filter(**my_filter).filter(game__home_field_team=2).filter(game__team_two=stad.team.id).annotate(Sum('touchdown')).annotate(Sum('tackle_for_loss')).annotate(Sum('fumble')).annotate(Sum('penalty'))
		if stad.stadium_name not in stads_done:
			if stad.first_year <= 2010:
				for i in range(2010,stad.last_year+1 if stad.last_year+1<=2018 else 2018):
					e = stad.stadium_name
					year1 = list(l1.filter(game__season=i))[0] if l1.filter(game__season=i) else blank_year
					year2 = list(l2.filter(game__season=i))[0] if l2.filter(game__season=i) else blank_year
					for k, v in stat_per_stad.items():
						stat_per_stad[k][i] += year1[k] +year2[k]
			else:
				for i in range(stad.first_year,stad.last_year+1 if stad.last_year+1<=2018 else 2018):
					e = stad.stadium_name
					year1 = list(l1.filter(game__season=i))[0] if l1.filter(game__season=i) else blank_year
					year2 = list(l2.filter(game__season=i))[0] if l2.filter(game__season=i) else blank_year
					for k, v in stat_per_stad.items():
						stat_per_stad[k][i] += year1[k] +year2[k]
					


			stadiums.append([stad.state, stad.city, stad.stadium_name, stad.stadium_lon, stad.stadium_lat, stad.super_bowl, stat_per_stad])
			stads_done.append(stad.stadium_name)
		else:
			if stad.first_year <= 2010:
				for i in range(2010,stad.last_year+1 if stad.last_year+1<=2018 else 2018):
					year1 = list(l1.filter(game__season=i))[0] if l1.filter(game__season=i) else blank_year
					year2 = list(l2.filter(game__season=i))[0] if l2.filter(game__season=i) else blank_year
					for k, v in stat_per_stad.items():	
						stadiums[stads_done.index(stad.stadium_name)][6][k][i] += year1[k] +year2[k]
			else:
				for i in range(stad.first_year,stad.last_year+1 if stad.last_year+1<=2018 else 2018):
					year1 = list(l1.filter(game__season=i))[0] if l1.filter(game__season=i) else blank_year
					year2 = list(l2.filter(game__season=i))[0] if l2.filter(game__season=i) else blank_year
					for k, v in stat_per_stad.items():						
						stadiums[stads_done.index(stad.stadium_name)][6][k][i] += year1[k] +year2[k]	

	return stadiums	


def passing_zones_filter(my_filter):
	passing_zones = list()
	passing_zones_complete = {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]}
	passing_zones_incomplete = {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[],2016:[],2017:[]}

	#short_left
	passing_zones.append(list(Football_Passing_Plays.objects.values('game__season').filter(**my_filter).filter(left=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete'))))
	
	#short_right
	passing_zones.append(list(Football_Passing_Plays.objects.values('game__season').filter(**my_filter).filter(right=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete'))))

	#short_middle
	passing_zones.append(list(Football_Passing_Plays.objects.values('game__season').filter(**my_filter).filter(middle=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete'))))

	#deep_left
	passing_zones.append(list(Football_Passing_Plays.objects.values('game__season').filter(**my_filter).filter(left=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete'))))

	#deep_right
	passing_zones.append(list(Football_Passing_Plays.objects.values('game__season').filter(**my_filter).filter(right=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete'))))
	
	#deep_middle
	passing_zones.append(list(Football_Passing_Plays.objects.values('game__season').filter(**my_filter).filter(middle=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete'))))
	

	for zone in passing_zones:
		for season in zone:
			for key,valye in passing_zones_complete.items():
				if key == season['game__season']:
					passing_zones_complete[key].append(season['complete__sum'])
					passing_zones_incomplete[key].append(season['incomplete__sum'])		

	return passing_zones_complete, passing_zones_incomplete


def fp_bkdwn(request, team_id):
	
	blank_year = {'yard_line':0, 'complete__sum':0, 'incomplete__sum': 0, 'touchdown__sum':0, 'interception__sum':0, 'pick_six__sum':0, 'fumble__sum':0, 'sack__sum':0, 'penalty__sum':0, 'yards__sum':0}
	opp_side = dict.fromkeys(['sl','sm','sr','dl','dm','dr'])
	own_side = dict.fromkeys(['sl','sm','sr','dl','dm','dr'])
	midfield = dict.fromkeys(['sl','sm','sr','dl','dm','dr'])
	field ={}
	per_yl = {
			'sl':blank_year,
			'sm':blank_year,
			'sr':blank_year,
			'dl':blank_year,
			'dm':blank_year,
			'dr':blank_year  
			}
	for i in range(1,100):
		field[i] = {}
		for t in range(2010,2018):
			field[i][t] = {}



	opp_side['sl'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=2).filter(left=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	opp_side['sm'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=2).filter(middle=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	opp_side['sr'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=2).filter(right=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	opp_side['dl'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=2).filter(left=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	opp_side['dm'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=2).filter(middle=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	opp_side['dr'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=2).filter(right=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))

	own_side['sl'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=1).filter(left=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	own_side['sm'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=1).filter(middle=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	own_side['sr'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=1).filter(right=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	own_side['dl'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=1).filter(left=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	own_side['dm'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=1).filter(middle=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	own_side['dr'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=1).filter(right=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	
	midfield['sl'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=0).filter(left=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	midfield['sm'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=0).filter(middle=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	midfield['sr'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=0).filter(right=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	midfield['dl'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=0).filter(left=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	midfield['dm'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=0).filter(middle=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	midfield['dr'] = list(Football_Passing_Plays.objects.values('yard_line','game__season').exclude(yard_line=0).filter(side_of_field=0).filter(right=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	
	# opp_side['sl'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=2).filter(left=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# opp_side['sm'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=2).filter(middle=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# opp_side['sr'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=2).filter(right=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# opp_side['dl'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=2).filter(left=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# opp_side['dm'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=2).filter(middle=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# opp_side['dr'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=2).filter(right=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))

	# own_side['sl'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=1).filter(left=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# own_side['sm'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=1).filter(middle=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# own_side['sr'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=1).filter(right=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# own_side['dl'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=1).filter(left=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# own_side['dm'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=1).filter(middle=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# own_side['dr'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=1).filter(right=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	
	# midfield['sl'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=0).filter(left=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# midfield['sm'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=0).filter(middle=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# midfield['sr'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=0).filter(right=1).filter(short=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# midfield['dl'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=0).filter(left=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# midfield['dm'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=0).filter(middle=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))
	# midfield['dr'] = list(Football_Passing_Plays.objects.values('yard_line').filter(game__season=y).filter(side_of_field=0).filter(right=1).filter(deep=1).annotate(Sum('complete')).annotate(Sum('incomplete')).annotate(Sum('touchdown')).annotate(Sum('interception')).annotate(Sum('pick_six')).annotate(Sum('penalty')).annotate(Sum('yards')).annotate(Avg('diff')))

	for k,v in opp_side.items():
		print(len(v))
		for t in range(len(v)):
			yl = v[t]['yard_line']
			year = v[t]['game__season']
			field[yl][year][k] = v[t]

	for k,v in midfield.items():
		for t in range(len(v)):
			yl = v[t]['yard_line']
			year = v[t]['game__season']
			field[yl][year][k] = v[t]

	for k,v in own_side.items():
		for t in range(len(v)):
			yl = 50+(50-v[t]['yard_line'])
			year = v[t]['game__season']
			field[yl][year][k] = v[t]	

	return render_to_response('fp_bkdwn.html', {'field':simplejson.dumps(field)})

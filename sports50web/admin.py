# Creates admin page which allows for easy visualization of model structure and data ingested
from django.contrib import admin

from .models import Sports
from .models import Teams
from .models import Stadiums
from .models import Positions
from .models import Players
from .models import GameLog
from .models import Football_Passing_Plays
from .models import Football_Rushing_Plays

@admin.register(Sports)
class SportsAdmin(admin.ModelAdmin):
	pass

@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
	pass

@admin.register(Stadiums)
class StadiumsAdmin(admin.ModelAdmin):
	pass

@admin.register(Positions)
class PositionsAdmin(admin.ModelAdmin):
	pass  

@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
	pass  

@admin.register(GameLog)
class GameLogAdmin(admin.ModelAdmin):
	pass  

@admin.register(Football_Passing_Plays)
class Football_Passing_PlaysAdmin(admin.ModelAdmin):
	list_display = ['player_id', 'complete', 'yards', 'touchdown', 'interception']

@admin.register(Football_Rushing_Plays)
class Football_Rushing_PlaysAdmin(admin.ModelAdmin):
	list_display = ['player_id', 'yards', 'touchdown', 'fumble']
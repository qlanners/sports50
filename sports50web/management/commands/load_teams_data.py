from csv import DictReader

from django.core.management import BaseCommand

from sports50web.models import Teams
from pytz import UTC


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from mlb_teams.csv into our Teams model"

    def handle(self, *args, **options):
        if Teams.objects.exists():
            print('Teams data already loaded...exiting.')
            return
        print("Loading teams data for current mlb teams")
        for row in DictReader(open('./mlb_teams.csv')):
            print(row.keys())
            team = Teams()
            team.sport = row['\ufeffSport']
            team.state = row['State']
            team.city = row['City']
            team.mascot = row['Mascot']
            team.abbrev = row['Abbreviation']
            team.first_year = row['First_Year']
            team.division = row['Division']
            team.level = row['Level']
            team.titles = row['Titles']
            team.save()

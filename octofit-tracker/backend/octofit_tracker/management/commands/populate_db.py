from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection
from datetime import date

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):

        # Clear existing data using Djongo's raw MongoDB access
        from django.db import connection
        db = connection.cursor().db_conn
        db['activities'].delete_many({})
        db['workouts'].delete_many({})
        db['leaderboard'].delete_many({})
        db['users'].delete_many({})
        db['teams'].delete_many({})

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (superheroes)
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        # Create activities
        Activity.objects.create(user=users[0], type='run', duration=30, date=date.today())
        Activity.objects.create(user=users[1], type='cycle', duration=45, date=date.today())
        Activity.objects.create(user=users[2], type='swim', duration=25, date=date.today())
        Activity.objects.create(user=users[3], type='yoga', duration=60, date=date.today())

        # Create workouts
        w1 = Workout.objects.create(name='Pushups', description='Do 20 pushups')
        w2 = Workout.objects.create(name='Situps', description='Do 30 situps')
        w1.suggested_for.set([users[0], users[2]])
        w2.suggested_for.set([users[1], users[3]])

        # Create leaderboard
        Leaderboard.objects.create(team=marvel, points=150)
        Leaderboard.objects.create(team=dc, points=120)


        # Ensure unique index on email using PyMongo
        from django.conf import settings
        from pymongo import MongoClient
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'], settings.DATABASES['default']['CLIENT']['port'])
        db = client[settings.DATABASES['default']['NAME']]
        db.users.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('Test data populated successfully.'))

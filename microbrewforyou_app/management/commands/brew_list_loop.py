from django.core.management.base import BaseCommand
from microbrewforyou_app.models import BrewTypes


class Command(BaseCommand):
    def handle(self, *args, **options):
        BREW_LIST = [
            # {"image":'images/amber_american_lagger.jpg'},
            {"name": 'Amber_American_Lager', "ABV": 5.25},
            {"name": 'German helles', "ABV": 4.8},
            {"name": 'Czech or bohemian pilsner', "ABV": 4.1},
            {"name": 'Amber Lager', "ABV": 4.8},
            {"name": 'Oktoberfest', "ABV": 5.1},
            {"name": 'German Schwarzbier', "ABV": 3.8},
            {"name": 'Vienna Lager', "ABV": 4.5},
            {"name": 'Traditional Bock', "ABV": 6.3},
            {"name": 'Doppelbock', "ABV": 6.6},
            {"name": 'Weizenbocks', "ABV": 7.0},
            {"name": 'Maibocks', "ABV": 6.0},
            {"name": 'American Brown Ale', "ABV": 4.2},
            {"name": 'English Brown Ale', "ABV": 4.0},
            {"name": 'American Amber Ale', "ABV": 4.4},
            {"name": 'American Pale Ale', "ABV": 4.4},
            {"name": 'Blonde Ales', "ABV": 4.1},
            {"name": 'English Bitters', "ABV": 3.0},
            {"name": 'English Pale Ales', "ABV": 4.5},
            {"name": 'American IPAs', "ABV": 6.3},
            {"name": 'Imperial or Double IPAs', "ABV": 7.0},
            {"name": 'English IPAs', "ABV": 5.0},
            {"name": 'American Imperial Porters', "ABV": 7.0},
            {"name": 'English Brown Porter', "ABV": 4.5},
            {"name": 'Robust Porters', "ABV": 5.1},
            {"name": 'American Stouts', "ABV": 5.7},
            {"name": 'American Imperial Stouts', "ABV": 7.0},
            {"name": 'Oatmeal Stout', "ABV": 3.8},
            {"name": 'Milk Stout', "ABV": 4.0},
            {"name": 'Irish Dry Stout', "ABV": 3.8},
            {"name": 'Belgian Pale Ale', "ABV": 4.0},
            {"name": 'Belgian Dubbels', "ABV": 6.3},
            {"name": 'Belgian Trippels', "ABV": 7.1},
            {"name": 'Belgian Quadrupels', "ABV": 7.2},
            {"name": 'Belgian Strong Dark Ale', "ABV": 4.8},
            {"name": 'Belgian Saison', "ABV": 4.4},
            {"name": 'American Pale Wheat Beer', "ABV": 3.5},
            {"name": 'Belgian Witbier', "ABV": 4.8},
            {"name": 'Berliner Weisse', "ABV": 2.8},
            {"name": 'Dunkelweizen', "ABV": 4.8},
            {"name": 'Hefeweizen', "ABV": 4.9},
            {"name": 'American Sour Beer', "ABV": 4.8},
            {"name": 'Belgian Fruit Lambics', "ABV": 5.0},
            {"name": 'Flanders Red Ale', "ABV": 4.8},
            {"name": 'Gueuzes', "ABV": 6.2},
        ]

        # loop through object and storing in dictionary
        for brew in BREW_LIST:
            BrewTypes.objects.create(name=brew["name"], averageABV=brew["ABV"])

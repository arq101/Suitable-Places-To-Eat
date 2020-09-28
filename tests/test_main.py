from argparse import Namespace
import pandas as pd
import pytest
import json
from pathlib import Path
import sys

import main


@pytest.fixture()
def json_user_data(tmpdir) -> Path:
    """ Fixture creates a json file with sample user data.
    """
    json_file = Path(tmpdir.mkdir('sub').join('users.json'))
    users = [
        {
            "name": "Foo",
            "wont_eat": ["Fish"],
            "drinks": ["Cider", "Rum", "Soft drinks"]
        },
        {
            "name": "Bar",
            "wont_eat": ["Eggs", "Pasta"],
            "drinks": ["Tequila", "Soft drinks", "beer", "Coffee"]
        }
    ]
    with open(json_file, 'w') as fh:
        json.dump(users, fh)
    return json_file


@pytest.fixture()
def csv_user_data(tmpdir) -> Path:
    """ Fixture creates a CSV source file with user data.
    """
    csv_file = Path(tmpdir.mkdir('sub').join('users.csv'))
    csv_file.write_text(
        'name,wont_eat,drinks\n'
        'Foo,Fish,"Cider,Rum,Soft drinks"\n'
    )
    return csv_file


@pytest.fixture()
def user_data() -> pd.DataFrame:
    """ Fixture creates dataframe sample user data.
    """
    users = [
        {
            "name": "user_Foobar",
            "wont_eat": ["Fish"],
            "drinks": ["Cider", "Rum", "Soft drinks"]
        },
        {
            "name": "user_Skunk",
            "wont_eat": ["Eggs", "Pasta"],
            "drinks": ["Tequila", "Soft drinks", "beer", "Coffee"]
        }
    ]
    df = pd.DataFrame(users, columns=['name', 'wont_eat', 'drinks'])
    return df


@pytest.fixture()
def venue_data() -> pd.DataFrame:
    """ Fixture creates dataframe with sample venue data.
    """
    venues = [
        {
            "name": "Eatery 1",
            "food": ["Fish", "BBQ"],
            "drinks": ["Soft drinks", "Tequila", "Beer"]
        },
        {
            "name": "Eatery 2",
            "food": ["Meat", "Vegetarian"],
            "drinks": ["Soft Drinks", "Rum", "Beer", "Whisky", "Cider"]
        },
        {
            "name": "Eatery 3",
            "food": ["Eggs", "Meat", "Fish", "Pasta", "Dairy"],
            "drinks": ["Vodka", "Gin", "whisky", "Rum", "Cider", "Beer", "Soft drinks"]
        },
    ]
    df = pd.DataFrame(venues, columns=['name', 'food', 'drinks'])
    return df


class TestPlacesToEatMain:

    def test_load_dataframe(self, json_user_data):
        outcome = main.load_dataframe(src_file=json_user_data)
        assert isinstance(outcome, pd.DataFrame)
        assert outcome.shape == (2, 3)

    def test_load_dataframe_unexpected_type(self, csv_user_data):
        with pytest.raises(ValueError) as err:
            main.load_dataframe(src_file=csv_user_data)
        assert err.match('Unexpected file type')

    def test_find_places_good_to_eat(self, user_data, venue_data):
        outcome = main.find_places_good_to_eat(users=user_data, venues=venue_data)
        expected = pd.DataFrame({
            'venue': ['Eatery 1', 'Eatery 2', 'Eatery 3'],
            'safe_to_eat_for': [['user_Skunk'], ['user_Foobar', 'user_Skunk'], []]
        })
        assert outcome.equals(expected)

    def test_places_to_visit(self, user_data):
        places_mapped = pd.DataFrame({
            'venue': ['Eatery 1', 'Eatery 2', 'Eatery 3'],
            'safe_to_eat_for': [['user_Skunk'], ['user_Foobar', 'user_Skunk'], []]
        })
        outcome = main.places_to_visit(mapped_places=places_mapped, users=user_data)
        expected = dict(places_to_visit=['Eatery 2'])
        assert outcome == expected

    def test_arg_parser(self, mocker):
        mocker.patch('sys.argv')
        sys.argv = ['program.py', '-u', './input_feeds/users.json', '-v', './input_feeds/venues.json']
        expected_args = Namespace(
            output='./result_places_to_go.json',
            users='./input_feeds/users.json',
            venues='./input_feeds/venues.json'
        )
        args = main.arg_parser()
        assert args == expected_args

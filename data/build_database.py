"""
This is a utility module to initialize, clean, and create the SQLite3 db.
"""

import os, sys

# adds __file__ parent dir (/yahtzee-app) to sys.path to enable config ref
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from yahtzee import db
from yahtzee.models import Game, User, UsersGames

# TODO: remove dummy data used to init/test the database
USERS = [
    {
        'username': 'paulmaclachlan',
        'password': 'password',
        'first_name': 'Paul',
        'last_name': 'Maclachlan',
        'email': 'test@test.com',
    },
    {
        'username': 'tayamaclachlan',
        'password': 'password',
        'first_name': 'Taya',
        'last_name': 'Maclachlan',
        'email': 'test@test.ca',
    }
]

GAMES = [
    {
    }
]

USERSGAMES = [
    {
        'ones': 0,
        'twos': 0,
        'threes': 0,
        'fours': 0,
        'fives': 0,
        'sixes': 0,
        'three_of_a_kind': 0,
        'four_of_a_kind': 0,
        'full_house': 0,
        'small_straight': 0,
        'large_straight': 0,
        'yahtzee': 0,
        'chance': 0,
        'yahtzee_bonus': 0,
        'top_score': 0,
        'top_bonus_score': 0,
        'top_bonus_score_delta': 0,
        'total_top_score': 0,
        'total_bottom_score': 0,
        'grand_total_score': 0,
        'user_id': 1,
        'game_id': 1
    },
    {
        'ones': 0,
        'twos': 0,
        'threes': 0,
        'fours': 0,
        'fives': 0,
        'sixes': 0,
        'three_of_a_kind': 0,
        'four_of_a_kind': 0,
        'full_house': 0,
        'small_straight': 0,
        'large_straight': 0,
        'yahtzee': 0,
        'chance': 0,
        'yahtzee_bonus': 0,
        'top_score': 0,
        'top_bonus_score': 0,
        'top_bonus_score_delta': 0,
        'total_top_score': 0,
        'total_bottom_score': 0,
        'grand_total_score': 0,
        'user_id': 2,
        'game_id': 1
    },
]

# delete database file if it already exists
if os.path.exists('./data/yahtzee.db'):
    os.remove('./data/yahtzee.db')

# create the database
db.create_all()

# iterate over the USERS dummy data and populate the users in the db
for user in USERS:
    u = User(
        username=user['username'],
        password=user['password'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        email=user['email']
        )
    db.session.add(u)

# iterate over GAMES dummy data and populate the games in the db
for game in GAMES:
    g = Game()
    db.session.add(g)

# iterate over the USERSGAMES dummy data and populate the users_games in the db
for user_game in USERSGAMES:
    ug = UsersGames(
        ones=user_game['ones'],
        twos=user_game['twos'],
        threes=user_game['threes'],
        fours=user_game['fours'],
        fives=user_game['fives'],
        sixes=user_game['sixes'],
        three_of_a_kind=user_game['three_of_a_kind'],
        four_of_a_kind=user_game['four_of_a_kind'],
        full_house=user_game['full_house'],
        small_straight=user_game['small_straight'],
        large_straight=user_game['large_straight'],
        yahtzee=user_game['yahtzee'],
        chance=user_game['chance'],
        yahtzee_bonus=user_game['yahtzee_bonus'],
        top_score=user_game['top_score'],
        top_bonus_score=user_game['top_bonus_score'],
        top_bonus_score_delta=user_game['top_bonus_score_delta'],
        total_top_score=user_game['total_top_score'],
        total_bottom_score=user_game['total_bottom_score'],
        grand_total_score=user_game['grand_total_score'],
        user_id=user_game['user_id'],
        game_id=user_game['game_id']
        )
    db.session.add(ug)

db.session.commit()

"""
This is a utility module to initialize, clean, and create the SQLite3 db.
"""

import os, sys, json

# adds __file__ parent dir (/yahtzee-app) to sys.path to enable config ref
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from yahtzee import db
from yahtzee.models import Game, User, UsersGames

# TODO: remove dummy data used to init/test the database
USERS = [
    {
        'username': 'paulmaclachlan',
        'password': '$2b$12$OfCz.7i1AMB5zfMgqzSam..LAT3t8B3ckst8WQMIIkEgVg8S27km6',
        'first_name': 'Paul',
        'last_name': 'Maclachlan',
        'email': 'test@test.com',
    },
    {
        'username': 'tayamaclachlan',
        'password': '$2b$12$OfCz.7i1AMB5zfMgqzSam..LAT3t8B3ckst8WQMIIkEgVg8S27km6',
        'first_name': 'Taya',
        'last_name': 'Maclachlan',
        'email': 'test@test.ca',
    }
]

# create build game state for turns, rolls, and rankings
test_game_state_python = {
                            "players": {
                                "player_1": {
                                    "user_id": 1,
                                    "turn": 1,
                                    "roll": 1,
                                    "rank": None
                                    },
                                "player_2": {
                                    "user_id": 2,
                                    "turn": 1,
                                    "roll": 1,
                                    "rank": None
                                    },
                                "player_3": {
                                    "user_id": None,
                                    "turn": None,
                                    "roll": None,
                                    "rank": None
                                    },
                                "player_4": {
                                    "user_id": None,
                                    "turn": None,
                                    "roll": None,
                                    "rank": None
                                    },
                            },
                            "turn_user_id": 1
                        }
test_game_state_json = json.dumps(test_game_state_python)

GAMES = [
    {
        "game_state": test_game_state_json
    }
]

USERSGAMES = [
    {
        'ones': 6,
        'user_id': 1,
        'game_id': 1
    },
    {
        'ones': 1,
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
    g = Game(
        game_state=game['game_state']
        )
    db.session.add(g)

# iterate over the USERSGAMES dummy data and populate the users_games in the db
for user_game in USERSGAMES:
    ug = UsersGames(
        ones=user_game['ones'],
        user_id=user_game['user_id'],
        game_id=user_game['game_id']
        )
    db.session.add(ug)

db.session.commit()

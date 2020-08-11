"""
This module contains the models for yahtzee. It also makes use of SQLAlchemy
"Model" class and Marshmallow "SQLAlchemyAutoSchema" class inheretence.
"""

from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

from yahtzee import db, ma, login_manager, app

import json


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UsersGames(db.Model):
    """
    UsersGames model which defines attributes for a user and game within the db

    UsersGames relationships: enables one-to-many between game and users
    """
    __tablename__ = "users_games"
    users_games_id = db.Column(db.Integer, nullable=False, primary_key=True)
    ones = db.Column(db.Integer, nullable=True)
    twos = db.Column(db.Integer, nullable=True)
    threes = db.Column(db.Integer, nullable=True)
    fours = db.Column(db.Integer, nullable=True)
    fives = db.Column(db.Integer, nullable=True)
    sixes = db.Column(db.Integer, nullable=True)
    three_of_a_kind = db.Column(db.Integer, nullable=True)
    four_of_a_kind = db.Column(db.Integer, nullable=True)
    full_house = db.Column(db.Integer, nullable=True)
    small_straight = db.Column(db.Integer, nullable=True)
    large_straight = db.Column(db.Integer, nullable=True)
    yahtzee = db.Column(db.Integer, nullable=True)
    chance = db.Column(db.Integer, nullable=True)
    yahtzee_bonus = db.Column(db.Integer, nullable=True)
    top_score = db.Column(db.Integer, nullable=True)
    top_bonus_score = db.Column(db.Integer, nullable=True)
    top_bonus_score_delta = db.Column(db.Integer, nullable=True)
    total_top_score = db.Column(db.Integer, nullable=True)
    total_bottom_score = db.Column(db.Integer, nullable=True)
    grand_total_score = db.Column(db.Integer, nullable=True)
    round_id = db.Column(db.Integer, nullable=False, default=1)
    roll = db.Column(db.Integer, nullable=False, default=1)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False
    )
    game_id = db.Column(
        db.Integer, db.ForeignKey('game.game_id'), nullable=False
    )

    def __repr__(self):
        return (
            f"UsersGames("
            f"'{self.users_games_id}', "
            f"'{self.user_id}', "
            f"'{self.game_id}', "
            f"'{self.ones}', "
            f"'{self.twos}', "
            f"'{self.threes}', "
            f"'{self.fours}', "
            f"'{self.fives}', "
            f"'{self.sixes}', "
            f"'{self.three_of_a_kind}', "
            f"'{self.four_of_a_kind}', "
            f"'{self.full_house}', "
            f"'{self.small_straight}', "
            f"'{self.large_straight}', "
            f"'{self.yahtzee}', "
            f"'{self.chance}', "
            f"'{self.yahtzee_bonus}', "
            f"'{self.top_score}', "
            f"'{self.top_bonus_score}', "
            f"'{self.top_bonus_score_delta}', "
            f"'{self.total_top_score}', "
            f"'{self.total_bottom_score}', "
            f"'{self.grand_total_score}', "
            f")"
        )


class UsersGamesSchema(ma.SQLAlchemyAutoSchema):
    """
    This UsersGames schema inherets from SQLAlchemyAutoSchema and uses the Meta
    class to find the SQLAlchemy model UsersGames and the db.session.
    """
    class Meta:
        model = UsersGames
        sqla_session = db.session


# UserMixin inheretence to provide LoginManager with:
# is_authenticate, is_active, is_anonymous, get_id
class User(db.Model, UserMixin):
    """
    User model which defines the user attributes and SQLite3 db table/fields.
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(
                        db.String(20),
                        nullable=False,
                        default='default.jpg'
                        )
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
        )
    users_games = db.relationship('UsersGames', backref='user', lazy=True)

    def __repr__(self):
        return (
            f"User('{self.id}', '{self.username}', '{self.first_name}', "
            f"'{self.last_name}', '{self.email}')"
        )

    def get_reset_token(self, expires_sec=1800):
        """
        Create a reset token for a user with an expiry.

        :param expires_sec: expiration time for token (default 1800 secs)
        :return: token
        """
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
        Verify reset token and try to return user.

        :param token: a token
        :return: user
        """
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class UserSchema(ma.SQLAlchemyAutoSchema):
    """
    This user schema inherets from SQLAlchemyAutoSchema and uses the Meta
    class to find the SQLAlchemy model User and the db.session.
    """
    class Meta:
        model = User
        sqla_session = db.session


class Game(db.Model):
    """
    Game model which defines the game attributes and db table/fields.
    """
    # create default JSON game_state to manage turns, rolls, and game ranks
    game_state_python = {
        "players": {
            "player_1": {
                "user_id": None,
                "turn": 1,
                "roll": 1,
                "rank": None
                },
            "player_2": {
                "user_id": None,
                "turn": 1,
                "roll": 1,
                "rank": None
                },
            "player_3": {
                "user_id": None,
                "turn": 1,
                "roll": 1,
                "rank": None
                },
            "player_4": {
                "user_id": None,
                "turn": 1,
                "roll": 1,
                "rank": None
                },
        },
        "turn_user_id": None
    }
    game_state_json = json.dumps(game_state_python)

    __tablename__ = "game"
    game_id = db.Column(db.Integer, nullable=False, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    game_state = db.Column(db.Text, nullable=False, default=game_state_json)
    users_games = db.relationship(
        'UsersGames',
        backref='game',
        lazy=True
        )

    def __repr__(self):
        return f"Game('{self.game_id}', '{self.timestamp}', "
        f"'{self.users_games}, {self.game_state}')"


class GameSchema(ma.SQLAlchemyAutoSchema):
    """
    This game schema inherets from SQLAlchemyAutoSchema and uses the Meta
    class to find the SQLAlchemy model Game and the db.session.
    """
    class Meta:
        model = Game
        sqla_session = db.session

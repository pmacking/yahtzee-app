from flask_wtf import FlaskForm
from wtforms import SubmitField


class RollDiceForm(FlaskForm):
    """Roll dice button utilized in usergame_round"""
    submit = SubmitField('Roll Dice')


class NewGameForm(FlaskForm):
    """
    This is the new game button utilized in read_games route

    :param FlaskForm: class inheretence from FlaskForm in flask_wtf
    """
    submit = SubmitField('New Game')


class CreateGameForm(FlaskForm):
    """
    This is the start new game form utilized in usersgames route

    :param FlaskForm: class inheretence from FlaskForm in flask_wtf
    """
    submit = SubmitField('Create Game')


class PlayGameForm(FlaskForm):
    """
    This is the play game form utilized in usergame route

    :param FlaskForm: class inheretence from FlaskForm in flask_wtf
    """
    submit = SubmitField('Play Game')

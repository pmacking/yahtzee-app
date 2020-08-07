from flask_wtf import FlaskForm
from wtforms import SubmitField


class CreateGameForm(FlaskForm):
    """
    This is the start new game form utilized in /usersgames route

    :param FlaskForm: class inheretence from FlaskForm in flask_wtf
    """
    # add attributes set to imported wtforms classes
    # included args '<Titlecase>' html label
    # add args as imported wtforms.validators classes with sub args as req
    submit = SubmitField('New Game')

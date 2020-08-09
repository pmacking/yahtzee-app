from flask import render_template, Blueprint, flash, redirect, url_for, abort
from flask_login import current_user, login_required

from yahtzee import db
from yahtzee.models import UsersGames, Game
from yahtzee.games.forms import CreateGameForm, PlayGameForm

import logging

# create logger and file_handler for logging user routes
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('yahtzee/logs/games.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# create games Blueprint instance for managing routing
games = Blueprint('games', __name__)


@games.route("/games", methods=['GET', 'POST'])
@login_required
def read_games():
    """
    This function responds to the URL /games
    """
    # display existing usersgames for current_user in template
    usersgames = UsersGames.query.\
        filter_by(user_id=current_user.id).\
        order_by(UsersGames.users_games_id.desc()).\
        all()

    # The above usergames object worked with a for loop in the template
    # Leaving this games query here as it returned the data expected
    # games = Game.query.\
    #     filter(Game.users_games.any(UsersGames.user_id == current_user.id)).\
    #     order_by(Game.game_id.desc()).\
    #     all()

    if not usersgames:
        return redirect(url_for('games.create_game'))

    return render_template(
        "read_games.html",
        title='Games',
        usersgames=usersgames
        )


@games.route("/games/new", methods=['GET', 'POST'])
@login_required
def create_game():
    """
    This function responds to the URL /games
    """

    form = CreateGameForm()

    if form.validate_on_submit():

        # create new game in db
        game = Game()
        try:
            db.session.add(game)
            db.session.commit()
            logger.info(f"New Game:{game.game_id}")
        except Exception as e:
            logger.exception(f'{e}')

        # create usersgames in db with relationship to game and current_user
        usersgame = UsersGames(
                    user_id=current_user.id,
                    game_id=game.game_id
                    )
        try:
            db.session.add(usersgame)
            db.session.commit()
            flash(f'New Game Started: {game.game_id}', 'success')
            logger.info(f"New UsersGames:{usersgame.users_games_id}")
        except Exception as e:
            logger.exception(f'{e}')

        # redirect user to new game
        return redirect(url_for(
                    'games.usergame',
                    game_id=game.game_id,
                    usergame_id=usersgame.users_games_id)
                    )

    return render_template(
        "create_game.html",
        title='New Game',
        form=form
        )


@games.route(
    "/games/<int:game_id>/usersgames/<int:usergame_id>",
    methods=['GET', 'POST']
    )
@login_required
def usergame(game_id, usergame_id):
    """
    This function responds to the URL /usersgames/<usergame>

    param: users_games_id from UserGames model
    """
    form = PlayGameForm()

    if form.validate_on_submit():
        return redirect(url_for(
            'games.usergame_turn',
            game_id=game_id,
            usergame_id=usergame_id)
            )

    usergame = UsersGames.query.get_or_404(usergame_id)

    # validate current_user is part of the game and usergame
    if game_id != usergame.game_id:
        abort(403)
    if usergame.user_id != current_user.id:
        abort(403)

    return render_template(
        "usergame.html",
        title=usergame.users_games_id,
        usergame=usergame,
        form=form
        )


@games.route(
    "/games/<int:game_id>/usersgames/<int:usergame_id>/turn",
    methods=['GET', 'POST']
    )
@login_required
def usergame_turn(game_id, usergame_id):
    """
    This function responds to the URL /usersgames/<usergame>

    param: users_games_id from UserGames model
    """
    usergame = UsersGames.query.get_or_404(usergame_id)

    # validate current_user is part of the game and usergame
    if game_id != usergame.game_id:
        abort(403)
    if usergame.user_id != current_user.id:
        abort(403)

    return render_template(
        "usergame_turn.html",
        title=usergame.users_games_id,
        usergame=usergame
        )

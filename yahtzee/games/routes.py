from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import current_user, login_required

from yahtzee import db
from yahtzee.models import UsersGames, Game
from yahtzee.games.forms import StartNewGameForm

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
def get_games():
    """
    This function responds to the URL /games
    """

    form = StartNewGameForm()

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
                    usergame_id=usersgame.users_games_id)
                    )

    # display existing usersgames for current_user in template
    usersgames = UsersGames.query.\
        filter_by(user_id=current_user.id).\
        order_by(UsersGames.users_games_id.desc()).\
        all()

    return render_template(
        "games.html",
        title='Games',
        usersgames=usersgames,
        form=form
        )


@games.route("/games/<usergame_id>", methods=['GET', 'POST'])
@login_required
def usergame(usergame_id):
    """
    This function responds to the URL /usersgames/<usergame>

    param: users_games_id from UserGames model
    """
    usergame = UsersGames.query.get_or_404(usergame_id)

    return render_template(
        "usergame.html",
        title=usergame.users_games_id,
        usergame=usergame
        )

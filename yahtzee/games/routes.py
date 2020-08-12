from flask import render_template, Blueprint, flash, redirect, url_for, abort
from flask_login import current_user, login_required

from yahtzee import db
from yahtzee.models import User, UsersGames, Game
from yahtzee.games.forms import (NewGameForm, CreateGameForm,
                                 PlayGameForm, RollDiceForm)
from yahtzee.games.utils import get_game_state_json

import logging, json

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
    form = NewGameForm()

    if form.validate_on_submit():
        return redirect(url_for('games.create_game'))

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

    # check if user has usersgame, and if not redirect to create a game
    if not usersgames:
        return redirect(url_for('games.create_game'))

    return render_template(
        "read_games.html",
        title='Games',
        usersgames=usersgames,
        form=form
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

        # update new game_state player_1 as current_user, and turn_user_id
        game_state_json = json.loads(game.game_state)
        game_state_json["players"]["player_1"]["user_id"] = current_user.id
        game_state_json["turn_user_id"] = current_user.id

        game.game_state = json.dumps(game_state_json)

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

    usergame = UsersGames.query.get_or_404(usergame_id)

    # get user whose turn it is
    game_state_json = get_game_state_json(usergame.game_id)
    turn_user_id = game_state_json["turn_user_id"]
    turn_user = User.query.get_or_404(turn_user_id)

    # validate current_user is part of the game and usergame
    if game_id != usergame.game_id:
        abort(403)
    if usergame.user_id != current_user.id:
        abort(403)

    if form.validate_on_submit():

        # validate it is current_user turn before redirect to play game
        if turn_user_id != current_user.id:
            flash(f"It is {turn_user.username}'s turn. Please wait for your "
                  f"turn.", 'danger')
        else:
            return redirect(url_for(
                'games.usergame_round',
                game_id=game_id,
                usergame_id=usergame_id,
                round_id=usergame.round_id)
                )

    return render_template(
        "usergame.html",
        title=usergame.game_id,
        usergame=usergame,
        turn_user=turn_user,
        form=form
        )


@games.route(
    "/games/<int:game_id>/usersgames/<int:usergame_id>/round/<int:round_id>",
    methods=['GET', 'POST']
    )
@login_required
def usergame_round(game_id, usergame_id, round_id):
    """
    This function responds to the URL /usersgames/<usergame>

    :param game_id: game_id from Game model
    :param usergame_id: users_games_id from UserGames model
    :param turn_id: turn count from from UserGames model
    """
    usergame = UsersGames.query.get_or_404(usergame_id)
    roll_id = usergame.roll_id

    # validate current_user is part of the game and usergame
    if game_id != usergame.game_id:
        abort(403)
    if usergame.user_id != current_user.id:
        abort(403)

    # get turn_user_id from game_state for validation
    game_state_json = get_game_state_json(usergame.game_id)
    turn_user_id = game_state_json["turn_user_id"]
    turn_user = User.query.get_or_404(turn_user_id)
    # get current_round from usergame for validation
    current_round = usergame.round_id

    # validate it's the current user's turn from game_state
    if turn_user_id != current_user.id:
        flash(f"It is {turn_user.username}'s turn. Please wait for your "
              f"turn.", 'danger')
        return redirect(url_for(
                    'games.usergame',
                    game_id=usergame.game_id,
                    usergame_id=usergame.usergame_id)
                    )

    # validate round_id is equivalent to current_round in usersgame
    if round_id != current_round:
        flash(f"Not the correct round. You are on round {current_round}",
              'danger')
        return redirect(url_for(
                    'games.usergame',
                    game_id=usergame.game_id,
                    usergame_id=usergame.users_games_id)
                    )

    form = RollDiceForm()

    if form.validate_on_submit():
        return redirect(url_for(
                    'games.round_roll',
                    game_id=usergame.game_id,
                    usergame_id=usergame_id,
                    round_id=usergame.round_id,
                    roll_id=roll_id)
                    )

    return render_template(
        "usergame_round.html",
        title=usergame.game_id,
        usergame=usergame,
        turn_user=turn_user,
        form=form
        )


@games.route(
    f"/games/<int:game_id>/usersgames/<int:usergame_id>/round/<int:round_id>"
    f"/roll/<int:roll_id>",
    methods=['GET', 'POST']
    )
@login_required
def round_roll(game_id, usergame_id, round_id, roll_id):
    """
    This function responds to the URL /usersgames/<usergame>

    :param game_id: game_id from Game model
    :param usergame_id: users_games_id from UserGames model
    :param turn_id: turn count from from UserGames model
    """
    usergame = UsersGames.query.get_or_404(usergame_id)
    roll_id = usergame.roll_id

    # validate current_user is part of the game and usergame
    if game_id != usergame.game_id:
        abort(403)
    if usergame.user_id != current_user.id:
        abort(403)

    # get turn_user_id from game_state for validation
    game_state_json = get_game_state_json(usergame.game_id)
    turn_user_id = game_state_json["turn_user_id"]
    turn_user = User.query.get_or_404(turn_user_id)
    # get current_round from usergame for validation
    current_round = usergame.round_id

    # validate it's the current user's turn from game_state
    if turn_user_id != current_user.id:
        flash(f"It is {turn_user.username}'s turn. Please wait for your "
              f"turn.", 'danger')
        return redirect(url_for(
                    'games.usergame',
                    game_id=usergame.game_id,
                    usergame_id=usergame.usergame_id)
                    )

    # validate round_id is equivalent to current_round in usersgame
    if round_id != current_round:
        flash(f"Not the correct round. You are on round {current_round}",
              'danger')
        return redirect(url_for(
                    'games.usergame',
                    game_id=usergame.game_id,
                    usergame_id=usergame.users_games_id)
                    )

    return render_template(
        "round_roll.html",
        title=usergame.game_id,
        usergame=usergame,
        turn_user=turn_user,
        )

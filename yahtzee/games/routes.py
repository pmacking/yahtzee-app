from flask import render_template, Blueprint
from flask_login import current_user, login_required

from yahtzee.models import UsersGames

games = Blueprint('games', __name__)


@games.route("/usersgames", methods=['GET', 'POST'])
# @login_required ensures /account page can only be accessed by authed users
@login_required
def usersgames():
    """
    This function responds to the URL /games
    """
    usersgames = UsersGames.query.\
        filter_by(user_id=current_user.id).\
        order_by(UsersGames.users_games_id.desc()).\
        all()

    return render_template("games.html", title='Games', usersgames=usersgames)


@games.route("/usersgames/<usergame>", methods=['GET', 'POST'])
# @login_required ensures /account page can only be accessed by authed users
@login_required
def usergame(usergame):
    """
    This function responds to the URL /usersgames/<usergame>

    param: users_games_id from UserGames model
    """

    return usergame

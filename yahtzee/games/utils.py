"""This module contains helper functions for games routes"""

import json

from yahtzee.models import Game


def get_game_state_json(game_id):
    """This function retrieves JSON game_state data from Game model.
    :param game_id: Game.game_id
    :return: game_state JSON data
    """
    # query game from game_id
    game = Game.query.\
        filter_by(game_id=game_id).\
        first()

    return json.loads(game.game_state)

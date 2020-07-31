"""
Main module to run the app.
"""

from yahtzee import app
from yahtzee.users.routes import users
from yahtzee.main.routes import main
from yahtzee.games.routes import games
from yahtzee.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(games)
app.register_blueprint(errors)

if __name__ == "__main__":
    app.run()

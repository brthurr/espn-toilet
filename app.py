from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.cli import with_appcontext
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from helpers.migrate_from_django import import_owners
from helpers.espn_api_helper import ESPNAPIHelper
from models import db, Owner

import click
import logging

app = Flask(__name__)
app.config.from_object('config.config.Config')

# Configure the logger
log_handler = logging.FileHandler(app.config['LOG_FILENAME'])
log_handler.setLevel(logging.getLevelName(app.config['LOG_LEVEL']))

# Set the formatter for the log handler
formatter = logging.Formatter(fmt=app.config['LOG_FORMAT'], datefmt=app.config['DATE_FORMAT'])
log_handler.setFormatter(formatter)

# Set the logger level and add the handler
app.logger.setLevel(logging.getLevelName(app.config['LOG_LEVEL']))
app.logger.addHandler(log_handler)

# Don't output to console
for handler in app.logger.handlers:
    app.logger.removeHandler(handler)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def hello_world():
    return 'Hello World'

@click.command(name='import_owners')
@click.option('--file', 'owners_file', required=True, type=str, help='Path and name of the JSON file with owner information')
@with_appcontext
def import_owners_command(owners_file):
    """
    Run this custom command to import owners from a JSON file.
    
    Args:
        owners_file (str): path and name of the JSON file with owner information
        
    """
    import_owners(owners_file, db, Owner)
    click.echo("Owners imported successfully.")

app.cli.add_command(import_owners_command)

@click.command(name='update_teams')
@click.option('--year', required=True, type=int, help='The year for which you want to update the teams.')  # Define 'year' as a command-line argument of type int
@with_appcontext
def update_teams_command(year):
    """
    Run this custom command to update teams for the given year.

    Args:
        year (int): The year for which you want to update the teams.
    """
    try:
        api_helper = ESPNAPIHelper(year)
        api_helper.update_teams()
        #click.echo(f"Teams imported successfully for {year}.")
    except Exception as e:
        click.echo(f"Unable to import teams: {str(e)}")

app.cli.add_command(update_teams_command)

@click.command(name='populate_tournament')
@click.option('--year', required=True, type=int, help='The year for which you want to populate the tournament.')  # Define 'year' as a command-line argument of type int
@with_appcontext
def populate_tournament_command(year):
    """
    Run this custom command to update teams for the given year.

    Args:
        year (int): The year for which you want to populate the tournament.
    """
    try:
        api_helper = ESPNAPIHelper(year)
        api_helper.populate_tournament()
        #click.echo(f"Teams imported successfully for {year}.")
    except Exception as e:
        click.echo(f"Unable to populate tournament: {str(e)}")

app.cli.add_command(populate_tournament_command)

if __name__ == '__main__':
    app.run()

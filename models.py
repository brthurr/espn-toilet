from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    espn_id = db.Column(db.String(50))
    name = db.Column(db.String(200))
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(12), nullable=True)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    espn_team_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    year = db.Column(db.Integer)
    name = db.Column(db.String(200))
    seed = db.Column(db.Integer)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    week = db.Column(db.Integer)
    round = db.Column(db.Integer)

    # Renaming these for clarity
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    # Scores can be nullable and updated after the game
    team1_score = db.Column(db.Integer, nullable=True)
    team2_score = db.Column(db.Integer, nullable=True)

    # Relationships
    team1 = db.relationship('Team', foreign_keys=[team1_id])
    team2 = db.relationship('Team', foreign_keys=[team2_id])

    status = db.Column(db.String(50))  # e.g., 'Scheduled', 'Completed', etc.
    # winner_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)


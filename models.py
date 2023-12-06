from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(12), nullable=True)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    year = db.Column(db.Integer)
    name = db.Column(db.String(200))
    seed = db.Column(db.Integer)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    week = db.Column(db.Integer)
    round = db.Column(db.Integer)
    loser_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    winner_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    loser_score = db.Column(db.Integer)
    winner_score = db.Column(db.Integer)

    loser_team = db.relationship('Team', foreign_keys=[loser_team_id])
    winner_team = db.relationship('Team', foreign_keys=[winner_team_id])

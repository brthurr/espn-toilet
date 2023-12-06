from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from models import db

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.config.Config')
print(app.config['SQLALCHEMY_DATABASE_URI'])

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run()

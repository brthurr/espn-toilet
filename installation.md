Create python virtual environment (pyEnv is GREAT for this!)
git clone git clone https://github.com/brthurr/toilet-v2 
pip install -r requirements.txt
create .env file
flask db migrate
flask db upgrade
populate owner table (flask import_owners --file <json>)
import teams (update_teams --year <year>)



Issues:

standings_weekly PR not yet accepted






pip install gunicorn
Create python virtual environment (pyEnv is GREAT for this!)
git clone git clone https://github.com/brthurr/toilet-v2 
pip install -r requirements.txt
create .env file
flask db migrate
flask db upgrade
populate owner table (flask import_owners --file <json>)
import teams (flask update_teams --year <year>)
populate_tournament (flask populate_tournament --year <year>)
if prior years:
    - update game results (flask update_game_results --start-week 15 --end-week 17 --year <year>)
    - update next round (flask update_tournament --start-week 15 --end-week 17 --year 2022)
    - Repeat for each round (this is clunky and I need to fix it)

test flask
    - change last line of app.py to app.run(host='0.0.0.0')
    - open firewall on server if necessary
    - test with public IP

follow https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04





Issues:

standings_weekly PR not yet accepted






pip install gunicorn
from espn_api.requests.espn_requests import ESPNAccessDenied, ESPNInvalidLeague
from espn_api.football import League
from flask import current_app
from models import db, Team, Owner, Game
from datetime import datetime
import traceback


class ESPNAPIHelper:
    def __init__(self, year):
        self.league_id = int(current_app.config["ESPN_LEAGUE_ID"])
        self.espn_s2 = current_app.config["ESPN_S2"]
        self.swid = current_app.config["SWID"]
        self.year = year

    def espn_api_call(self):
        """
        Makes and API call to the ESPN Fantasy Football API

        Keyword arguments:
        year - Year to pull league data

        Return: Object containing all relevant league/player data for the year provided
        """

        try:
            self.league = League(
                league_id=self.league_id,
                year=self.year,
                espn_s2=self.espn_s2,
                swid=self.swid,
            )
        except (ESPNInvalidLeague, ESPNAccessDenied, Exception) as e:
            self.league = None
            current_app.logger.error(f"Failed to fetch league data: {e}")

        return self.league

    def update_teams(self):
        """
        Update the Team table with the current year's team information from the ESPN API.
        """

        # Fetch league data
        try:
            league = self.espn_api_call()
        except Exception as e:
            current_app.logger.error(f"Error fetching league data: {e}")
            return

        if league is None:
            current_app.logger.error(
                "League data is not available. Cannot update teams."
            )
            return

        for api_team in league.teams:
            # Process each team
            try:
                # Extract owner_sid
                owner_sid = self.extract_owner_sid(api_team)
                if owner_sid is None:
                    continue

                # Find the owner in the Owner table by sid
                owner = Owner.query.filter_by(espn_id=owner_sid).first()
                if owner is None:
                    current_app.logger.error(f"No owner found with sid: {owner_sid}")
                    continue

                # Update Team table
                self.update_or_add_team(api_team, owner)

            except Exception as e:
                current_app.logger.error(
                    f"Error processing team {api_team.team_name}: {e}"
                )

    def extract_owner_sid(self, api_team):
        """
        Extracts the owner SID from the api_team object.
        """
        try:
            owner_sid_list = api_team.owners
            if owner_sid_list and isinstance(owner_sid_list, list):
                owner_sid_dict = owner_sid_list[0]
                return owner_sid_dict.get("id")
            else:
                current_app.logger.error(
                    f"Invalid ESPN ID format for team: {api_team.team_name}"
                )
                return None
        except Exception as e:
            current_app.logger.error(
                f"Error extracting ESPN ID for team {api_team.team_name}: {e}"
            )
            return None

    def update_or_add_team(self, api_team, owner):
        """
        Updates an existing team or adds a new team to the database.
        """
        try:
            team = Team.query.filter_by(owner_id=owner.espn_id, year=self.year).first()
            if team is None:
                team = Team(
                    owner_id=owner.espn_id, year=self.year, name=api_team.team_name
                )
                db.session.add(team)
                db.session.commit()
                current_app.logger.info(f"Added new team: {team.name} for {self.year}")
            elif team.name != api_team.team_name:
                team.name = api_team.team_name
                db.session.commit()
                current_app.logger.info(
                    f"Updated team name: {team.name} for {self.year}"
                )
        except Exception as e:
            current_app.logger.error(
                f"Error updating/adding team for owner {owner.name}: {e}"
            )

    def get_league_standings(self, league, week=None):
        
        standings_data = {}
        
        # Fetch league data
        try:
            if week is None:
                self.week = league.current_week
            else:
                self.week = week
                
            standings = league.standings_weekly(week)
            
            standings_data = {
                'week': week,
                'standings': standings
            }
            
            return standings_data
        
        except Exception as e:
            current_app.logger.error(f"Error fetching league standings: {e}")
            return
        
    def populate_tournament(self):
        try:
            league = self.espn_api_call()
            #current_app.logger.info(league)
            if league.year != datetime.now().year:
                week = 14
            else:
                if league.current_week != 14: # Last week of the regular season
                    current_app.logger.info("League is still in the regular season.")
                    return
                
            league_standings = self.get_league_standings(league, week)
            current_app.logger.info(league_standings)
        
            if league_standings:
                # Fetch and store team IDs for seeds 7 through 12
                team_ids_for_seeds = {}
                for index, team in enumerate(league_standings['standings'], start=1):
                    if 7 <= index <= 12:
                        db_team = Team.query.filter_by(name=team.team_name, year=self.year).first()
                        if db_team:
                            team_ids_for_seeds[index] = db_team.id
                        else:
                            current_app.logger.warning(f"Team '{team.team_name}' for year {self.year} not found in database.")

                # Create games for round 1 (seeds 7 vs 10 and 8 vs 9)
                for match in [(7, 10), (8, 9)]:
                    team1_id = team_ids_for_seeds.get(match[0])
                    team2_id = team_ids_for_seeds.get(match[1])
                    if team1_id and team2_id:
                        game = Game(year=self.year, week=week, round=1, team1_id=team1_id, team2_id=team2_id)
                        db.session.add(game)
                        current_app.logger.info(f"Added new game: Seeds {match[0]} vs. {match[1]} for {self.year}")

                # Create placeholder games for round 2 with seeds 11 and 12
                for seed in [11, 12]:
                    team_id = team_ids_for_seeds.get(seed)
                    if team_id:
                        game = Game(year=self.year, week=week, round=2, team1_id=team_id)
                        db.session.add(game)
                        current_app.logger.info(f"Added placeholder game for Seed {seed} in Round 2 for {self.year}")

                db.session.commit()
                        
        except Exception as e:
            tb = traceback.format_exc()
            current_app.logger.exception(f"Error populating tournament: {e}\n{tb}")
            return

    def get_tb_teams(self):
        # Your logic to get Toilet Bowl participants from Django
        pass

    def collate_results(self):
        # Your logic to match Django results with corresponding ESPN scores
        pass

    def update_scores(self):
        # Your logic to update scores in the Django DB
        pass

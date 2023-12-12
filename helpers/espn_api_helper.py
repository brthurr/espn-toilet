from espn_api.requests.espn_requests import ESPNAccessDenied, ESPNInvalidLeague
from espn_api.football import League
from flask import current_app
from models import db, Team, Owner, Game
from datetime import datetime
from sqlalchemy.orm import aliased
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

        # TODO: Update seed (additional method?)

        try:
            team = Team.query.filter_by(owner_id=owner.espn_id, year=self.year).first()
            if team is None:
                team = Team(
                    owner_id=owner.espn_id,
                    year=self.year,
                    name=api_team.team_name,
                    espn_team_id=api_team.team_id,
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
        """
        Calculates league standings for use in other methods.
        Calls custom method standings_weekly() in espn_api (not yet integrated 12/2023) # TODO: Submit PR (done 12/11/2023)

        Args:
            league (obj): ESPN FF API league object
            week (int, optional): week to pull standings. Mostly to populate previoud league tournaments. Defaults to None.

        Returns:
            dict: Dictionary object comprised of a week number and a list of ESPN team objects.
        """

        standings_data = {}

        # Fetch league data
        try:
            if week is None:
                self.week = league.current_week
            else:
                self.week = week

            standings = league.standings_weekly(week)

            standings_data = {"week": week, "standings": standings}

            return standings_data

        except Exception as e:
            current_app.logger.error(f"Error fetching league standings: {e}")
            return

    def populate_tournament(self):
        try:
            league = self.espn_api_call()
            if league.year != datetime.now().year:
                week = 14
            else:
                if league.current_week != 14:  # Last week of the regular season
                    current_app.logger.info("League is still in the regular season.")
                    return

            league_standings = self.get_league_standings(league, week)

            if league_standings:
                # Fetch and store team IDs for seeds 7 through 12
                team_ids_for_seeds = {}
                for index, team in enumerate(league_standings["standings"], start=1):
                    if 7 <= index <= 12:
                        db_team = Team.query.filter_by(
                            name=team.team_name, year=self.year
                        ).first()
                        if db_team:
                            team_ids_for_seeds[index] = db_team.id
                        else:
                            current_app.logger.warning(
                                f"Team '{team.team_name}' for year {self.year} not found in database."
                            )

                # Create games for round 1 (seeds 7 vs 10 and 8 vs 9)
                for match in [(7, 10), (8, 9)]:
                    team1_id = team_ids_for_seeds.get(match[0])
                    team2_id = team_ids_for_seeds.get(match[1])
                    if team1_id and team2_id:
                        game = Game(
                            year=self.year,
                            week=week,
                            round=1,
                            team1_id=team1_id,
                            team2_id=team2_id,
                        )
                        db.session.add(game)
                        current_app.logger.info(
                            f"Added new game: Seeds {match[0]} vs. {match[1]} for {self.year}"
                        )

                # Create placeholder games for round 2 with seeds 11 and 12
                for seed in [11, 12]:
                    team_id = team_ids_for_seeds.get(seed)
                    if team_id:
                        game = Game(
                            year=self.year, week=week + 1, round=2, team1_id=team_id
                        )
                        db.session.add(game)
                        current_app.logger.info(
                            f"Added placeholder game for Seed {seed} in Round 2 for {self.year}"
                        )

                db.session.commit()

        except Exception as e:
            tb = traceback.format_exc()
            current_app.logger.exception(f"Error populating tournament: {e}\n{tb}")
            return

    def get_tb_teams(self):
        try:
            """
            Get Toilet Bowl participants from Flask for a given year.
            """
            Team1 = aliased(Team)
            Team2 = aliased(Team)

            tb_teams = (
                Game.query.filter_by(year=self.year)
                .join(Team1, Game.team1_id == Team1.id)
                .join(Team2, Game.team2_id == Team2.id, isouter=True)
                .add_columns(
                    Team1.id.label("team1_id"),
                    Team1.name.label("team1_name"),
                    Team1.espn_team_id.label("team1_espn_team_id"),
                    Team2.id.label("team2_id"),
                    Team2.name.label("team2_name"),
                    Team2.espn_team_id.label("team2_espn_team_id"),
                )
                .all()
            )

            tb_list = []
            for (
                game,
                team1_id,
                team1_name,
                team1_espn_team_id,
                team2_id,
                team2_name,
                team2_espn_team_id,
            ) in tb_teams:
                tb_list.append(
                    {
                        "week": game.week,
                        "round": game.round,
                        "team1_id": team1_id,
                        "team1_name": team1_name,
                        "team1_espn_team_id": team1_espn_team_id,
                        "team2_id": team2_id,
                        "team2_name": team2_name,
                        "team2_espn_team_id": team2_espn_team_id,
                    }
                )
            return tb_list

        except Exception as e:
            tb = traceback.format_exc()
            current_app.logger.exception(
                f"Error getting TB teams: {e}\n{tb}. Have you populated the tournament for the year?"
            )
            return

    def update_game_results(self, week):
        """
        Update the toilet bowl game results for the given weeks.

        Args:
            weeks_to_update (list): List of weeks to update results.

        Returns:
            None
        """
        # TODO: Write logic to check if score hasn't changed (saves DB write)
        # TODO: Update status of game depending on day of the week (In Progress Thursday = Monday, Final on Tuesday)
        try:
            teams = self.espn_api_call().teams
            if self.league is not None:
                team_id_to_team = {team.team_id: team for team in teams}

                for tb_team in self.get_tb_teams():
                    if (
                        tb_team["team1_espn_team_id"]
                        and tb_team["team1_espn_team_id"] is not None
                        and tb_team["team2_espn_team_id"]
                        and tb_team["team2_espn_team_id"] is not None
                    ):
                        if (
                            tb_team["team1_espn_team_id"]
                            and tb_team["team1_espn_team_id"] is not None
                        ):
                            espn_id_1 = tb_team["team1_espn_team_id"]
                            espn_id_2 = tb_team["team2_espn_team_id"]
                            current_app.logger.info(f"Team 1 ESPN ID: {espn_id_1}")
                            current_app.logger.info(f"Team 2 ESPN ID: {espn_id_2}")

                            # Access specific teams by their IDs using the dictionary
                            team_1 = team_id_to_team[espn_id_1]
                            team_2 = team_id_to_team[espn_id_2]
                            if team_1 is None or team_2 is None:
                                current_app.logger.error("Team not found.")
                                continue

                            try:
                                team_score_1 = team_1.scores[
                                    week - 1
                                ]  # Adjust for week
                                team_score_2 = team_2.scores[
                                    week - 1
                                ]  # Adjust for week
                            except IndexError:
                                current_app.logger.error(
                                    f"Index out of range for week {week}"
                                )
                                continue
                            current_app.logger.info(f"Team 1 Score: {team_score_1}")
                            current_app.logger.info(f"Team 2 Score: {team_score_2}")

                            game_1 = Game.query.filter_by(
                                year=self.year,
                                week=week,
                                round=tb_team["round"],
                                team1_id=tb_team["team1_id"],
                            ).first()  # Use .first() to get the game object

                            if game_1 is None:
                                current_app.logger.error("Game not found.")
                                continue
                            game_1.team1_score = team_score_1  # Update team1_score
                            game_1.team2_score = team_score_2  # Update team1_score
                            db.session.commit()
                            current_app.logger.info(
                                f"Updated game with score for {tb_team['team1_name']} and {tb_team['team2_name']} for {self.year} (Week {week})"
                            )
        except Exception as e:
            tb = traceback.format_exc()
            current_app.logger.exception(f"Error updating game results: {e}\n{tb}")
            return

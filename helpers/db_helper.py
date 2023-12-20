import pandas as pd
from flask import current_app
from datetime import datetime, timedelta


def import_schedule(year, db, Schedule):
    url = f"https://www.pro-football-reference.com/years/{year}/games.htm"

    df = df = pd.read_html(url)[0]
    df = df.copy()

    # Convert 'Week' column to numeric, errors='coerce' will set non-numeric values to NaN
    df["Week"] = pd.to_numeric(df["Week"], errors="coerce")

    # Drop rows where 'Week' is NaN (non-integer weeks)
    df = df.dropna(subset=["Week"])

    # Convert 'Date' and 'Time' columns to datetime objects for accurate comparison
    df["DateTime"] = pd.to_datetime(
        df["Date"] + " " + df["Time"], format="%Y-%m-%d %I:%M%p"
    )

    # Filtering the DataFrame to include only weeks 15, 16, and 17
    df_filtered = df[df["Week"].isin([15, 16, 17])]

    # Finding the earliest and latest games for weeks 15, 16, and 17
    selected_weeks_earliest_and_latest = (
        df_filtered.groupby("Week")["DateTime"].agg(["min", "max"]).reset_index()
    )

    selected_weeks_earliest_and_latest["min"] = pd.to_datetime(
        selected_weeks_earliest_and_latest["min"]
    )

    # Function to find the previous Tuesday at 00:01 for a given datetime
    def get_previous_tuesday(date):
        # Calculate the number of days to subtract to get to the previous Tuesday
        days_to_subtract = (date.weekday() - 1) % 7
        if days_to_subtract == 0:  # If today is Tuesday, go back a full week
            days_to_subtract = 7
        previous_tuesday = date - pd.Timedelta(days=days_to_subtract)
        # Set the time to 00:01
        previous_tuesday = previous_tuesday.replace(
            hour=0, minute=1, second=0, microsecond=0
        )
        return previous_tuesday

    # Apply the function
    selected_weeks_earliest_and_latest[
        "week_start"
    ] = selected_weeks_earliest_and_latest["min"].apply(get_previous_tuesday)

    for index, row in selected_weeks_earliest_and_latest.iterrows():
        schedule = Schedule.query.filter_by(year=year, week=row["Week"]).first()
        if schedule is None:
            new_schedule = Schedule(
                year=year,
                week=int(row["Week"]),
                early_game_date_time=row["min"].isoformat(),
                late_game_date_time=row["max"].isoformat(),
                week_start=row["week_start"].isoformat(),
            )
            db.session.add(new_schedule)
            db.session.commit()  # Commit for each schedule entry
            current_app.logger.info(f"Week {row['Week']} of {year} added.")
        else:
            current_app.logger.warning(
                f"Week {row['Week']} of {year} already exists. Skipping..."
            )


def return_week_dates(year, db, Schedule):
    # Example query to retrieve the schedule
    schedule = Schedule.query.filter_by(year=year).all()

    formatted_schedule = []

    for game in schedule:
        # Convert the string to a datetime object
        early_game_time = datetime.fromisoformat(game.early_game_date_time)
        late_game_time = datetime.fromisoformat(game.late_game_date_time)
        week_start = datetime.fromisoformat(game.week_start)

        # Format the datetime object
        early_formatted_time = early_game_time.strftime("%b %d")
        late_formatted_time = late_game_time.strftime("%b %d")
        week_start_formatted_time = week_start.strftime("%m/%d/%Y %H:%M:%S")

        formatted_schedule.append(
            {
                "week": game.week,
                "year": game.year,
                "early_game": early_formatted_time,
                "late_game": late_formatted_time,
                "week_start": week_start,
            }
        )
    return formatted_schedule


def get_current_round(scheduled_game):  # year was old argument
    try:
        # league = self.espn_api_call()
        # if self.league is not None:
        if scheduled_game is not None:
            if scheduled_game["year"] == datetime.now().year:
                week = scheduled_game["week_start"]
                print(week)
                one_week_out = week + timedelta(weeks=1)
                two_weeks_out = week + timedelta(weeks=2)
                if week >= one_week_out:
                    round = 1
                elif week < one_week_out <= two_weeks_out:
                    round = 2
                elif week >= two_weeks_out:
                    round = 3
            else:
                round = 3
        print(round)
        return round
    except Exception as e:
        current_app.logger.error(f"Unable to fetch current round. {e}")
        return

import pandas as pd
from flask import current_app


def import_schedule(year, db, Schedule):
    url = f"https://www.pro-football-reference.com/years/{year}/games.htm"

    df = df = pd.read_html(url)[0]

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

    for index, row in selected_weeks_earliest_and_latest.iterrows():
        schedule = Schedule.query.filter_by(year=year, week=row["Week"]).first()
        if schedule is None:
            new_schedule = Schedule(
                year=year,
                week=int(row["Week"]),  # Convert to int for safety
                early_game_date_time=row[
                    "min"
                ].isoformat(),  # Convert Timestamp to string
                late_game_date_time=row[
                    "max"
                ].isoformat(),  # Convert Timestamp to string
            )
            db.session.add(new_schedule)
            db.session.commit()  # Commit for each schedule entry
            current_app.logger.info(f"Week {row['Week']} of {year} added.")
        else:
            current_app.logger.warning(
                f"Week {row['Week']} of {year} already exists. Skipping..."
            )

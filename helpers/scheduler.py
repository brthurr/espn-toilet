from datetime import datetime, time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import subprocess

scheduler = BackgroundScheduler(daemon=True)


def update_game_results_job():
    now = datetime.now()
    current_time = now.time()
    current_day = now.weekday()  # Monday is 0, Sunday is 6

    # Define the time bounds
    start_time = time(19, 0)  # 7 PM
    end_time = time(23, 0)  # 11 PM

    # Check if current time is within the desired timeframe
    if (
        (current_day == 3 and current_time >= start_time)
        or (current_day == 0 and current_time <= end_time)
        or (0 < current_day < 3)
    ):
        try:
            # Get the current year
            current_year = datetime.now().year

            # Define the command to run, using the current year
            command = [
                "flask",
                "update_game_results",
                "--start-week",
                "15",
                "--end-week",
                "17",
                f"--year={current_year}",  # Use the current year in the command
            ]

            # Run the Flask command as a subprocess
            subprocess.run(command, check=True)

        except Exception as e:
            # Handle any exceptions that may occur during the command execution
            print(f"Error running Flask command: {e}")
    else:
        return


def update_tournament_command_job():
    try:
        current_year = datetime.now().year
        command = [
            "flask",
            "update_tournament",
            "--start-week",
            "15",
            "--end-week",
            "17",
            f"--year={current_year}",
        ]
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"Error running Flask command: {e}")


# Schedule for update_game_results_job
scheduler.add_job(
    update_game_results_job,
    trigger=CronTrigger(hour="0-23", day_of_week="thu, fri, sat, sun, mon"),
)

scheduler.add_job(
    update_tournament_command_job,
    trigger=CronTrigger(day_of_week="tue", hour=3, minute=0),
)

scheduler.start()

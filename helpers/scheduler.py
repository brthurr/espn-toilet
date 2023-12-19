from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import subprocess

scheduler = BackgroundScheduler(daemon=True)


def update_game_results_job():
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


def update_tournament_command():
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
    trigger=IntervalTrigger(minutes=5),
)

# Schedule for update_tournament_command
scheduler.add_job(
    update_tournament_command,
    trigger=CronTrigger(day_of_week="tue", hour=3, minute=0),
)

scheduler.start()

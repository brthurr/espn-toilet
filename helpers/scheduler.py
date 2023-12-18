from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
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


scheduler.add_job(
    update_game_results_job,
    trigger=IntervalTrigger(minutes=5),
)
scheduler.start()

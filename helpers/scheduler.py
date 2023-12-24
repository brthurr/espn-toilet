from datetime import datetime, time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import OrTrigger
import subprocess
import logging
import os

scheduler = BackgroundScheduler(daemon=True)

# Logging configuration
LOG_FILENAME = "./logs/scheduler.log"
LOG_LEVEL = "DEBUG"  # Adjust this based on your needs
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

if not os.path.isfile(LOG_FILENAME):
    open(LOG_FILENAME, "a").close()

logging.basicConfig(level=LOG_LEVEL, filename=LOG_FILENAME, filemode='a', format=LOG_FORMAT, datefmt=DATE_FORMAT)


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
            logging.info(f"Update game results command ran successfully.")

        except Exception as e:
            # Handle any exceptions that may occur during the command execution
            logging.error(f"Error running Flask command: {e}")
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
        logging.info(f"Update tournament command ran successfully.")
    except Exception as e:
        logging.error(f"Error running Flask command: {e}")


# Schedule for update_game_results_job
scheduler.add_job(
    update_game_results_job,
    trigger=OrTrigger([
        CronTrigger(hour="19-23", minute="*/5", day_of_week="thu, mon"),
        CronTrigger(hour="11-23", minute="*/5", day_of_week="fri, sat, sun"),
    ])
)

scheduler.add_job(
    update_tournament_command_job,
    trigger=CronTrigger(day_of_week="tue", hour=3, minute=0),
)

scheduler.start()

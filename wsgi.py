from helpers.scheduler import update_game_results_job
from app import app

if __name__ == "__main__":
    update_game_results_job()  # Start the scheduler
    app.run()

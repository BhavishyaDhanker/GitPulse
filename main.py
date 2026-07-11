import logging
import time
import functools

from watchdog.observers import Observer

import config
import git_handler
from monitor import GitPulseHandler


def setup_logging(verbose_level):
    level_map = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }
    level = level_map.get(verbose_level, logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("GitLogs.txt"),
            logging.StreamHandler()
        ]
    )


def main():
    try:
        cfg = config.load_config()
    except (FileNotFoundError, ValueError, KeyError) as e:
        print(f"Failed to load configuration: {e}")
        return

    setup_logging(cfg["verbose_level"])
    logger = logging.getLogger(__name__)

    repo_path = cfg["repo_path"]
    idle_duration = cfg["idle_duration"]
    push_enabled = cfg["push_enabled"]

    commit_callback = functools.partial(
        git_handler.commit_changes, repo_path, push_enabled
    )

    event_handler = GitPulseHandler(
        idle_duration=idle_duration,
        commit_callback=commit_callback,
        repo_path=repo_path
    )

    observer = Observer()
    observer.schedule(event_handler, str(repo_path), recursive=True)
    observer.start()

    logger.info("GitPulse is now running. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutdown signal received. Stopping observer.")
        observer.stop()
    finally:
        observer.join()
        logger.info("GitPulse has stopped.")


if __name__ == "__main__":
    main()
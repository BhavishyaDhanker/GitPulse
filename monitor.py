from watchdog.events import PatternMatchingEventHandler
import threading
import logging
logger = logging.getLogger(__name__)

class GitPulseHandler(PatternMatchingEventHandler):
    def __init__(self, idle_duration, commit_callback, repo_path):
        super().__init__(ignore_patterns=["*/.git/*", "*/.git"])
        self._idle_duration = idle_duration
        self._commit_callback = commit_callback
        self._timer = None
        self._lock = threading.Lock()
        logger.info(f"Started monitoring repository: {repo_path}")



    def on_any_event(self, event):
        logger.debug(
            f"Event detected: {event.event_type} -> {event.src_path}"
        )
        if self._timer is not None:
            self._timer.cancel()
            logger.debug("File change detected. Resetting idle timer.")
        self._timer = threading.Timer(

            self._idle_duration, 
            self._trigger_commit
        )
        logger.debug(
            f"Idle timer started ({self.idle_duration}s)"
        )
        self._timer.start()



    def _trigger_commit(self):
        logger.info(
            "Repository idle. Triggering automated commit."
        )

        if not self._lock.acquire(blocking=False):
            logger.warning(
                "Commit already in progress. Ignoring trigger."
            )
            return
        try:

            self._commit_callback()
        except Exception as e:
            logger.error(f"Error during commit callback: {e}")
        finally:
            self._lock.release()




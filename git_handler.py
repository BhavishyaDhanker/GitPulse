import logging
import subprocess
logger = logging.getLogger(__name__)

def _run_git_command(args, repo_path):
    logger.debug(f"Running command: git {' '.join(args)}")
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        logger.debug(f"Command completed: git {' '.join(args)}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {' '.join(e.cmd)}")
        raise RuntimeError(f"Git command failed: {e.stderr.strip()}") from e
    

def _has_changes(repo_path):
    logger.debug("Checking repository for uncommitted changes.")
    status_output = _run_git_command(["status", "--porcelain"], repo_path)
    return bool(status_output)

def _git_add(repo_path):
    _run_git_command(["add", "."], repo_path)
    logger.info("Staged all changes.")

def _git_commit(message, repo_path):
    _run_git_command(["commit", "-m", message], repo_path)
    logger.info("Commit created successfully.")

def _git_push(repo_path, push_enabled):
    try:
        if push_enabled:
            logger.info("Pushing commits to remote repository.")
            _run_git_command(["push"], repo_path)
        else:
            logger.info("Push is disabled in the configuration. Skipping push.")
    except RuntimeError as e:
        logger.exception(f"Error during push operation: {e}")
        raise


def commit_changes(repo_path, push_enabled):
    logger.info("Starting automated commit process.")
    try:
        if _has_changes(repo_path):
            logger.info("Changes detected. Preparing commit.")
            _git_add(repo_path)
            _git_commit("Automated commit by GitPulse", repo_path)
            _git_push(repo_path, push_enabled)
        else:
            logger.info("No changes detected. Skipping commit.")
    except RuntimeError as e:
        logger.exception(f"Error during Git operation: {e}")
        logger.exception("Automated commit process failed.")


import logging

def setup_logging(verbose_level):

    level_mapping = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }
    level = level_mapping.get(verbose_level, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(name)s -%(message)s",
        handlers=[
            logging.FileHandler("GitLogs.txt", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
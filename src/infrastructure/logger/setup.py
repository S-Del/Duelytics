from datetime import date
from logging import DEBUG, basicConfig, getLogger, INFO, FileHandler, Formatter
from os.path import join
from pathlib import Path


def init_logger():
    basicConfig(level=INFO)
    logger = getLogger()
    if logger.handlers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    log_dir = Path("log")
    log_dir.mkdir(exist_ok=True)
    log_path = join(log_dir, f"{str(date.today())}.log")

    file_handler = FileHandler(log_path, encoding="utf-8")
    formatter = Formatter(
        "%(asctime)s [%(levelname)s] %(module)s:%(lineno)d > %(message)s",
        datefmt="%H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

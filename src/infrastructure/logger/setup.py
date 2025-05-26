from datetime import date
from logging import DEBUG, basicConfig, getLogger, INFO, FileHandler, Formatter
from os.path import join
from pathlib import Path
import sys


def init_logger():
    # pyinstaller によってバンドルされたバイナリかどうか判定している
    is_bundle = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
    if is_bundle:
        level = INFO
    else:
        level = DEBUG

    basicConfig(level=level)
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

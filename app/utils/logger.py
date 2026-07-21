import logging
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


LOG_FILE = (
    f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
)

LOG_PATH = LOG_DIR / LOG_FILE


logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format=(
        "[%(asctime)s] "
        "%(levelname)s | "
        "%(filename)s:%(lineno)d | "
        "%(message)s"
    ),
)


logger = logging.getLogger("study-agent")
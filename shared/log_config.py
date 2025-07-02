from loguru import logger
import os

def setup_logging():
    logger.remove()

    logger.add(
        "sys.stderr",
        level="INFO",
        format="{time} {level} {message}",
        colorize=True
    )

    log_file_path = os.path.join("logs", "bot_log_{time}.log")
    logger.add(
        log_file_path,
        rotation="50 MB",
        compression="zip",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        enqueue=True,
        retention="7 days"
    )

    logger.info("Logging setup complete.")

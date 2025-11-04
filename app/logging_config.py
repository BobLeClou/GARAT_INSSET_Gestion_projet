import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # log vers console (docker logs)
            logging.FileHandler("app.log", mode='a', encoding='utf-8', delay=False)
        ]
    )
    logger = logging.getLogger("app_logger")
    return logger

logger = setup_logger()

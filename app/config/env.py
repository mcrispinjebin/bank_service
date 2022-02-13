import os
import sys
import logging

DB_URL = ""
DB_NAME = ""
DB_USER = ""
DB_PASS = ""


def initialize_env():
    global DB_URL, DB_NAME, DB_USER, DB_PASS

    DB_URL = os.environ.get("DB_URL")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")

    if not DB_URL:
        logging.error("DB_URL is not set")
        sys.exit(99)
    elif not DB_NAME:
        logging.error("DB_NAME is not set")
        sys.exit(99)
    elif not DB_USER:
        logging.error("DB_USER is not set")
        sys.exit(99)
    elif not DB_PASS:
        logging.error("DB_PASS is not set")
        sys.exit(99)
    logging.info("Environment is loaded successfully")

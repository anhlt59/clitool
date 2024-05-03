import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
AWS_IGNORED_PROFILES = ("cli_session",)
AWS_CREDENTIALS_DIR = os.getenv("AWS_CREDENTIALS_DIR", "~/.aws")
AWS_DEFAULT_PROFILE = os.getenv("AWS_DEFAULT_PROFILE", "default")
AWS_DEFAULT_SESSION_PROFILE = os.getenv("AWS_DEFAULT_SESSION_PROFILE", "cli_session")

CACHE_FILE = os.getenv("CACHE_FILE") or os.path.join(BASE_DIR, ".cache")
CUSTOM_FILE = os.getenv("CUSTOM_FILE") or os.path.join(BASE_DIR, "custom.json")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR") or os.path.join(BASE_DIR, "downloads")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "<%(module)s.%(funcName)s:%(lineno)s> - %(message)s"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"

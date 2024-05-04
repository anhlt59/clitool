import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
AWS_IGNORED_PROFILES = ("cli_session",)
AWS_CREDENTIALS_DIR = os.getenv("AWS_CREDENTIALS_DIR", "~/.aws")
AWS_DEFAULT_PROFILE = os.getenv("AWS_DEFAULT_PROFILE", "default")
AWS_DEFAULT_SESSION_PROFILE = os.getenv("AWS_DEFAULT_SESSION_PROFILE", "cli_session")
# fmt: off
AWS_REGIONS = {"us-east-1", "us-east-2", "us-west-1", "us-west-2", "af-south-1", "ap-east-1", "ap-south-1", "ap-northeast-3", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1", "ca-central-1", "cn-north-1", "cn-northwest-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-south-1", "eu-west-3", "eu-north-1", "me-south-1", "sa-east-1"}  # noqa
# fmt: on

CACHE_FILE = os.getenv("CACHE_FILE") or os.path.join(BASE_DIR, ".cache")
CUSTOM_FILE = os.getenv("CUSTOM_FILE") or os.path.join(BASE_DIR, "custom.json")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR") or os.path.join(BASE_DIR, "downloads")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "<%(module)s.%(funcName)s:%(lineno)s> - %(message)s"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"

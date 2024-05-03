import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DUMMY_DIR = os.path.join(BASE_DIR, "tests", "dummy")

os.environ["AWS_CONFIG_FILE"] = os.path.join(BASE_DIR, "tests", "dummy", ".aws", "config")
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = os.path.join(BASE_DIR, "tests", "dummy", ".aws", "credentials")
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

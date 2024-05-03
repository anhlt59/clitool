from .cloudformation import cli as cloudformation
from .dynamodb import cli as dynamodb
from .iam import cli as iam
from .lambda_ import cli as lambda_
from .s3 import cli as s3
from .secrets_manager import cli as secrets_manager
from .session import cli as session

__all__ = ["iam", "session", "cloudformation", "s3", "lambda_", "secrets_manager", "dynamodb"]

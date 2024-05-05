from .cloudformation import cli as cloudformation
from .dynamodb import cli as dynamodb
from .ecr import cli as ecr
from .iam import cli as iam
from .lambda_ import cli as lambda_
from .s3 import cli as s3
from .secrets_manager import cli as secrets_manager
from .session import cli as session

__all__ = ["cloudformation", "dynamodb", "ecr", "iam", "lambda_", "s3", "secrets_manager", "session"]

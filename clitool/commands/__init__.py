from .cloudformation import cli as cloudformation
from .dynamodb import cli as dynamodb
from .iam import cli as iam
from .lambda_ import cli as lambda_
from .s3 import cli as s3
from .secretsmanager import cli as secretsmanager
from .session import cli as session

__all__ = ["iam", "session", "cloudformation", "s3", "lambda_", "secretsmanager", "dynamodb"]

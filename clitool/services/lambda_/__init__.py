from clitool.services.base import AwsService

from .function import LambdaFunctionService
from .layer import LambdaLayerService


class LambdaService(AwsService):
    def __init__(self, session):
        super().__init__(session)
        self.function = LambdaFunctionService(session)
        self.layer = LambdaLayerService(session)


__all__ = ["LambdaService"]

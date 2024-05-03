from clitool.base import SingletonMeta
from clitool.services.session import SessionService


class AwsService(metaclass=SingletonMeta):
    session: SessionService

    def __init__(self, session: SessionService, *args, **kwargs):
        self.session = session

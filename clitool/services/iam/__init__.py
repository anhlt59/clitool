from clitool.services.base import AwsService
from clitool.services.session import SessionService

from .custom import IamCustomService
from .policy import IamPolicyService
from .role import IamRoleService


class IamService(AwsService):
    def __init__(self, session: SessionService):
        super().__init__(session)
        self.role = IamRoleService(session)
        self.policy = IamPolicyService(session)
        self.custom = IamCustomService(session)


__all__ = ["IamService"]

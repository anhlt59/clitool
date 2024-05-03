from click_shell import shell

from clitool.services import IamService, SessionService

session = SessionService()
iam = IamService(session)


# CLI commands ---------------------------------------------------------------
@shell("policy", prompt="AWS ❯ IAM ❯ Policy ❯ ")
def cli():
    pass

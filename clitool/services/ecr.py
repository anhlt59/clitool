from clitool.services.base import AwsService
from clitool.types.ecr import EcrRepositories, EcrRepository


class EcrService(AwsService):
    @property
    def client(self):
        return self.session.client("ecr")

    def list_repos(self, prefix: str = "") -> EcrRepositories:
        """
        List ECR repositories.
        :param prefix: Name prefix to filter by.
        """
        repos = EcrRepositories()
        response = self.client.describe_repositories()
        for repo in response.get("repositories", []):
            if prefix and not repo.get("repositoryName", "").startswith(prefix):
                continue
            repos.append(
                EcrRepository(
                    name=repo.get("repositoryName"),
                    arn=repo.get("repositoryArn"),
                    id=repo.get("registryId"),
                    uri=f"https://{repo.get('registryId')}.dkr.ecr.{self.session.profile.region}.amazonaws.com",
                )
            )
        return repos

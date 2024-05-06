from clitool.services.base import AwsService
from clitool.types.ecr import EcrImage, EcrImages, EcrRepositories, EcrRepository


class EcrService(AwsService):
    @property
    def client(self):
        return self.session.client("ecr")

    def create_repository(self, repository_name: str) -> EcrRepository:
        """
        Create an ECR repository.
        :param repository_name: Name of the repository.
        """
        response = self.client.create_repository(
            repositoryName=repository_name,
            tags=[{"Key": "CreatedBy", "Value": "CliTool"}],
        )
        return EcrRepository(
            name=response["repository"].get("repositoryName"),
            arn=response["repository"].get("repositoryArn"),
            uri=response["repository"].get("repositoryUri"),
            registry_id=response["repository"].get("registryId"),
            created_at=response["repository"].get("createdAt"),
        )

    def list_repositories(self, prefix: str = "") -> EcrRepositories:
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
                    uri=f"https://{repo.get('registryId')}.dkr.ecr.{self.session.profile.region}.amazonaws.com",
                    registry_id=repo.get("registryId"),
                    created_at=repo.get("createdAt"),
                )
            )
        return repos

    def list_images(self, repository_name: str):
        """
        List ECR images.
        :param repository_name: Name of the repository.
        """
        images = EcrImages()
        response = self.client.list_images(repositoryName=repository_name)
        if image_ids := response.get("imageIds", []):
            response = self.client.describe_images(repositoryName=repository_name, imageIds=image_ids)

            for image in response.get("imageDetails", []):
                images.append(
                    EcrImage(
                        registry_id=image.get("registryId"),
                        repository_name=repository_name,
                        image_digest=image.get("imageDigest"),
                        image_tags=image.get("imageTag"),
                        image_size_in_bytes=image.get("imageSizeInBytes"),
                        image_pushed_at=image.get("imagePushedAt"),
                        last_pulled_at=image.get("lastRecordedPullTime"),
                    )
                )
        return images

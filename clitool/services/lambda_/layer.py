import os
import re

from clitool.constants import BASE_DIR, LAYER_ARN_PATTERN, PYTHON_SUPPORTED_RUNTIMES
from clitool.services.base import AwsService
from clitool.types.lambda_ import LambdaLayer, LambdaLayers, PublishLayerConfig, Runtimes
from clitool.utils import execute_command


class LambdaLayerService(AwsService):
    @property
    def client(self):
        return self.session.client("lambda")

    def get(self, name: str) -> LambdaLayer:
        # Describe the layer to get its latest version
        response = self.client.list_layer_versions(LayerName=name)
        # Sort the versions by version number in descending order
        layer_versions = sorted(response["LayerVersions"], key=lambda x: x["Version"], reverse=True)
        # Extracting the latest version number
        latest_version = layer_versions[0]
        matched_reg = re.search(LAYER_ARN_PATTERN, latest_version["LayerVersionArn"])
        arn = matched_reg.string if matched_reg else latest_version["LayerVersionArn"]
        return LambdaLayer(
            name=name,
            arn=arn,
            description=latest_version["Description"],
            version=latest_version["Version"],
            created_date=latest_version["CreatedDate"],
            runtimes=latest_version["CompatibleRuntimes"],
        )

    def list(self, runtime: Runtimes | None = None, name_filter: str = "") -> LambdaLayers:
        """
        List all Lambda layers in the account.
        Parameters:
            runtime (str): The runtime to filter by.
            name_filter (str): The name of the Lambda layer to filter by.
        Returns:
            dict: A dictionary containing the list of Lambda layers.
        """

        def _list(_name_filter: str = "", **_kwargs):
            response = self.client.list_layers(**_kwargs)
            for layer in response.get("Layers", []):
                if _name_filter and _name_filter not in layer["LayerName"]:
                    continue
                if version := layer["LatestMatchingVersion"]:
                    yield LambdaLayer(
                        name=layer["LayerName"],
                        arn=layer["LayerArn"],
                        description=version.get("Description", ""),
                        version=version.get("Version"),
                        created_date=version.get("CreatedDate"),
                        runtimes=version.get("CompatibleRuntimes", []),
                    )
            if response.get("NextMarker"):
                _kwargs.update(Marker=response["NextMarker"])
                yield from _list(_name_filter, **_kwargs)

        kwargs = {"CompatibleRuntime": runtime} if runtime else {}
        layers = _list(name_filter, **kwargs)
        return LambdaLayers(list(layers))

    def publish(self, config: PublishLayerConfig):
        """Publish a Lambda layer to the account."""
        response = self.client.publish_layer_version(
            LayerName=config.name,
            Description=config.description,
            Content={
                "S3Bucket": config.archive.s3_bucket,
                "S3Key": config.archive.s3_key,
            },
            CompatibleRuntimes=config.runtimes,
        )
        return LambdaLayer(
            name=config.name,
            arn=response["LayerArn"],
            description=config.description,
            version=response["Version"],
            created_date=response["CreatedDate"],
            runtimes=config.runtimes,
            content=LambdaLayer.Content(
                sha=response["Content"]["CodeSha256"],
                size=response["Content"]["CodeSize"],
                location=response["Content"]["Location"],
            ),
        )

    @staticmethod
    def export_python_layer(runtime: str, requirement_file: str):
        """Export a Lambda layer to the specified directory."""
        if not os.path.isfile(requirement_file):
            raise FileNotFoundError(f"Requirement file not found: {requirement_file}")
        if runtime not in PYTHON_SUPPORTED_RUNTIMES:
            raise ValueError(f"Unsupported runtime: {runtime}")

        # Run script `export_python_layer.sh` to export a Lambda layer
        runtime = "python312" if runtime == "python3.12" else "python38-311"
        script_path = os.path.join(BASE_DIR, "scripts", "export_python_layer.sh")
        execute_command(f"{script_path} {runtime} {requirement_file}", "STDOUT")

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from clitool.types import CliItem, CliItems, CliTable

# fmt: off
Runtimes = Literal["nodejs", "nodejs4.3", "nodejs6.10", "nodejs8.10", "nodejs10.x", "nodejs12.x", "nodejs14.x", "nodejs16.x", "java8", "java8.al2", "java11", "python2.7", "python3.6", "python3.7", "python3.8", "python3.9", "dotnetcore1.0", "dotnetcore2.0", "dotnetcore2.1", "dotnetcore3.1", "dotnet6", "dotnet8", "nodejs4.3-edge", "go1.x", "ruby2.5", "ruby2.7", "provided", "provided.al2", "nodejs18.x", "python3.10", "java17", "ruby3.2", "ruby3.3", "python3.11", "nodejs20.x", "provided.al2023", "python3.12", "java21"]  # noqa
FunctionState = Literal["Pending", "Active", "Inactive", "Failed"]
# fmt: on


@dataclass
class LambdaFunction(CliItem):
    @dataclass
    class VpcConfig:
        vpc_id: str
        subnet_ids: list[str]
        security_group_ids: list[str]
        # ipv6_allowed_for_dual_stack: bool

    @dataclass
    class Environment:
        variables: dict[str, str]

    @dataclass
    class Layer:
        arn: str
        code_size: int
        # signing_profile_version_arn: str
        # signing_job_arn: str

    @dataclass
    class LoggingConfig:
        log_format: str
        log_group: str
        # application_log_level: str
        # system_log_level: str

    @dataclass
    class Code:
        location: str
        repository_type: str
        image_uri: str
        resolved_image_uri: str

    name: str
    arn: str
    runtime: str
    role: str
    handler: str
    description: str
    timeout: int
    memory_size: int
    ephemeral_storage: int
    last_modified: datetime
    version: str
    vpc_config: VpcConfig
    environment: Environment
    layers: list[Layer]
    logging_config: LoggingConfig


@dataclass
class LambdaExecutionResult(CliItem):
    status_code: int
    function_error: str
    log_result: str
    payload: str
    executed_version: str


@dataclass
class PublishLayerConfig:
    @dataclass
    class PublishLayerArchive:
        s3_bucket: str | None = None
        s3_key: str | None = None
        s3_object_version: str | None = None
        zip_file: bytes | None = None

    name: str
    runtimes: list[Runtimes]
    archive: PublishLayerArchive
    description: str = ""


@dataclass
class LambdaLayer(CliItem):
    @dataclass
    class Content:
        sha: str
        size: int
        location: str

    name: str
    arn: str
    description: str
    version: int
    created_date: str
    # license: str
    runtimes: list[Runtimes]
    content: Content | None = None


class LambdaLayers(CliItems):
    item_class = LambdaLayer


class LambdaFunctions(CliItems):
    item_class = LambdaFunction


class LambdaLayerTable(CliTable):
    item_class = LambdaLayer


class LambdaFunctionTable(CliTable):
    item_class = LambdaFunction

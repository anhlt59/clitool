import json
from datetime import datetime

from clitool.services.base import AwsService
from clitool.types.lambda_ import LambdaExecutionResult, LambdaFunction, LambdaFunctions


class LambdaFunctionService(AwsService):
    @property
    def client(self):
        return self.session.client("lambda")

    def invoke(self, function_name: str, payload: dict):
        """
        Invoke a Lambda function and get its result.
        Parameters:
            function_name (str): The name or ARN of the Lambda function.
            payload (dict): The payload to be passed to the Lambda function.
        Returns:
            dict: The result returned by the Lambda function.
        """
        response = self.client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",  # Synchronous invocation
            Payload=json.dumps(payload),
        )
        # Extracting the result from the response
        response["Payload"].read().decode("utf-8")
        return LambdaExecutionResult(
            status_code=response["StatusCode"],
            function_error=response["FunctionError"],
            log_result=response["LogResult"],
            payload=response["Payload"].read().decode("utf-8"),
            executed_version=response["ExecutedVersion"],
        )

    def list(self, name_filter: str = "") -> LambdaFunctions:
        """
        List all Lambda functions in the account.
        Parameters:
            name_filter (str): The name of the Lambda function to filter by.
        Returns:
            dict: A dictionary containing the list of Lambda functions.
        """
        functions = LambdaFunctions()
        response = self.client.list_functions()
        for function in response["Functions"]:
            if name_filter and name_filter not in function["FunctionName"]:
                continue
            functions.append(
                LambdaFunction(
                    name=function["FunctionName"],
                    arn=function["FunctionArn"],
                    runtime=function["Runtime"],
                    role=function["Role"],
                    handler=function["Handler"],
                    description=function["Description"],
                    timeout=function["Timeout"],
                    memory_size=function["MemorySize"],
                    ephemeral_storage=function["EphemeralStorage"]["Size"],
                    last_modified=datetime.strptime(function["LastModified"], "%Y-%m-%dT%H:%M:%S.%f%z"),
                    version=function["Version"],
                    vpc_config=LambdaFunction.VpcConfig(
                        vpc_id=function["VpcConfig"]["VpcId"],
                        subnet_ids=function["VpcConfig"]["SubnetIds"],
                        security_group_ids=function["VpcConfig"]["SecurityGroupIds"],
                    ),
                    environment=LambdaFunction.Environment(variables=function["Environment"]["Variables"]),
                    layers=[
                        LambdaFunction.Layer(
                            arn=layer["Arn"],
                            code_size=layer["CodeSize"],
                        )
                        for layer in function["Layers"]
                    ],
                    logging_config=LambdaFunction.LoggingConfig(
                        log_format=function["LoggingConfig"]["LogFormat"],
                        log_group=function["LoggingConfig"]["LogGroup"],
                    ),
                )
            )
        return functions

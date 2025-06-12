from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    Duration,
    RemovalPolicy
)
from constructs import Construct
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode

class MessageProcessorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.Table(
            self, "MessagesTable",
            partition_key=dynamodb.Attribute(name="messageUUID", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        lambda_fn = DockerImageFunction(
            self, "MessageProcessorFunction",
            code=DockerImageCode.from_image_asset(directory="lambda_function"),
            timeout=Duration.seconds(10),
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        table.grant_write_data(lambda_fn)

        api = apigateway.LambdaRestApi(
            self, "MessageProcessorAPI",
            handler=lambda_fn,
            proxy=False
        )

        messages = api.root.add_resource("messages")
        messages.add_method("POST")

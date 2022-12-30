from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)

from cdk_dynamo_table_view import TableViewer
from .hitcounter import HitCounter


class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_lambda = _lambda.Function(
            self, 'lgpy-lambda',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler',
        )

        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstreamFn=my_lambda,
        )

        apigw.LambdaRestApi(
            self, 'LGEndpoint',
            handler=hello_with_counter.handler,
        )

        TableViewer(
            self, 'LGViewHitCounter',
            title='Hello Hits',
            table=hello_with_counter.table,
        )

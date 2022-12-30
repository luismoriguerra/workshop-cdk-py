from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    RemovalPolicy,
)


class HitCounter(Construct):

    @property
    def handler(self):
        return self._hitCounterFn

    @property
    def table(self):
        return self._table

    def __init__(self, scope: Construct, id: str, downstreamFn: _lambda.IFunction, **kwargs):
        super().__init__(scope, id, **kwargs)

        self._table =  ddb.Table(
            self, 'LGHits',
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY,
        )

        self._hitCounterFn = _lambda.Function(
            self, 'LGHitCounterHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='hitcounter.handler',
            code=_lambda.Code.from_asset('lambda'),
            environment={
                'DOWNSTREAM_FUNCTION_NAME': downstreamFn.function_name,
                'HITS_TABLE_NAME': self._table.table_name,
            },
        )

        self._table.grant_read_write_data(self._hitCounterFn)
        downstreamFn.grant_invoke(self._hitCounterFn)

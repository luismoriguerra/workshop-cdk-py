import json
import os
import boto3

tableName = os.environ['HITS_TABLE_NAME']
downstreamFn = os.environ['DOWNSTREAM_FUNCTION_NAME']

ddb = boto3.resource('dynamodb')
table = ddb.Table(tableName)

_lambda = boto3.client('lambda')


def hander(event, context):
    print('request {}'.format(json.dumps(event)))
    table.update_item(
        key={'path': event['path']},
        UpdateExpression='ADD hits :incr',
        ExpressionAttributeValues={':incr': 1},
    )

    resp = _lambda.invoke(
        FunctionName=downstreamFn,
        Payload=json.dumps(event),
    )

    body = resp['Payload'].read()

    print('downstream response: {}'.format(body))
    return json.loads(body)

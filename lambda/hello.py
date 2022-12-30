
import json


def handler(event, request):
    print('request {}'.format(json.dumps(event)))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain',
        },
        'body': 'Good night from Lambda {}\n!'.format(event['path']),
    }

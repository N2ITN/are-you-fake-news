from cosine_dist import *
import json


def lambda_handler(url, context=None):
    print(url)
    result = orchestrate(url['body'])
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(dict(result))
    }
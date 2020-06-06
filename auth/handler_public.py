import json


def lambda_function(event, context):
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True,},
        "body": json.dumps({"message": "Hi from Public API"}),
    }

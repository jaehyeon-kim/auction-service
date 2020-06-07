import re
from src.authorize import get_decode_token, generate_policy


def lambda_function(event, context):
    print(event)  # keys: type (eg TOKEN), methodArn (apig arn), authorizationToken
    if not event.get("authorizationToken"):
        raise Exception("Unauthorized")

    token = re.sub(r"^Bearer ", "", event["authorizationToken"])

    try:
        decoded_token = get_decode_token(token)
        policy = generate_policy(decoded_token=decoded_token, method_arn=event["methodArn"])
        print(policy)
        return policy
    except Exception as e:
        print(e)
        raise Exception("Unauthorized")


if __name__ == "__main__":
    import os

    event = {"type": "TOKEN", "authorizationToken": os.getenv("TOKEN"), "methodArn": "foo/bar"}
    lambda_function(event, {})

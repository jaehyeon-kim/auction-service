import re
from authorize import get_decode_token, generate_policy


def lambda_function(event, context):
    if not event.get("authorizationToken"):
        raise Exception("Unauthorized")

    token = re.sub(r"^Bearer ", "", event["authorizationToken"])

    try:
        decoded_token = get_decode_token(token)
        policy = generate_policy(principal_id=decoded_token["sub"], method_arn=event["methodArn"])
        print(policy)
        return policy
    except Exception as e:
        print(e)
        raise Exception("Unauthorized")

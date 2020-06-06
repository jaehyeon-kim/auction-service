import os
import json
from urllib.request import urlopen
from jose import jwt

# https://aws.amazon.com/premiumsupport/knowledge-center/decode-verify-cognito-json-token/
# https://www.alexdebrie.com/posts/lambda-custom-authorizers/
# https://github.com/codingly-io/serverless-auth0-authorizer

USER_POOL_ID = os.getenv("USER_POOL_ID", "ap-southeast-2_he47XQ6v9")
APP_CLIENT_ID = os.getenv("APP_CLIENT_ID", "52qq2fbu4j363i73mpo2lkbanf")
AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")
COGNITO_ISSUER = f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{USER_POOL_ID}"
ALGORITHMS = ["RS256"]


class TokenDecodeException(Exception):
    pass


def get_json_web_key_sets():
    resp = urlopen(f"{COGNITO_ISSUER}/.well-known/jwks.json")
    return json.loads(resp.read().decode())


def get_rsa_key(token: str):
    rsa_key = None
    unverified_header = jwt.get_unverified_header(token)
    jwks = get_json_web_key_sets()
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if not rsa_key:
        raise Exception("fails to fine RSA Key")
    return rsa_key


def get_decode_token(token: str):
    try:
        rsa_key = get_rsa_key(token)
        decoded_token = jwt.decode(
            token=token,
            key=rsa_key,
            algorithms=ALGORITHMS,
            issuer=COGNITO_ISSUER,
            audience=APP_CLIENT_ID,
        )
        return decoded_token
    except (jwt.ExpiredSignatureError, jwt.JWTClaimsError) as e:
        raise TokenDecodeException(e)


def generate_policy(principal_id: str, method_arn: str):
    return {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": f'{next(iter(method_arn.split("/")))}/*/*',
                }
            ],
        },
    }


if __name__ == "__main__":
    from pprint import pprint

    id_token = os.getenv("ID_TOKEN")
    if id_token:
        pprint(get_decode_token(id_token))

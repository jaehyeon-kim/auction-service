import os
from pprint import pprint
import boto3

client = boto3.client("cognito-idp")

APP_CLIENT_ID = os.getenv("APP_CLIENT_ID", "52qq2fbu4j363i73mpo2lkbanf")
USERNAME = os.getenv("USERNAME", "dottami@gmail.com")
PASSWORD = os.getenv("PASSWORD", "Passw0rd")


def init_auth():
    return client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": USERNAME, "PASSWORD": PASSWORD},
        ClientId=APP_CLIENT_ID,
    )


if __name__ == "__main__":
    print("init auth...")
    pprint(init_auth()["AuthenticationResult"])

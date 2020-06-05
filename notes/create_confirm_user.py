import os
import time
import boto3

client = boto3.client("cognito-idp")

USER_POOL_ID = os.getenv("USER_POOL_ID", "ap-southeast-2_he47XQ6v9")
APP_CLIENT_ID = os.getenv("APP_CLIENT_ID", "52qq2fbu4j363i73mpo2lkbanf")
USERNAME = os.getenv("USERNAME", "dottami@gmail.com")
PASSWORD = os.getenv("PASSWORD", "Passw0rd")


def create_user():
    return client.sign_up(ClientId=APP_CLIENT_ID, Username=USERNAME, Password=PASSWORD)


def confirm_sign_up():
    return client.admin_confirm_sign_up(UserPoolId=USER_POOL_ID, Username=USERNAME)


if __name__ == "__main__":
    print("create user...")
    print(create_user())
    time.sleep(0.5)
    print("confirm sign up...")
    print(confirm_sign_up())

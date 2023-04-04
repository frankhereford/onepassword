#!/usr/bin/env python3
import os
import hashlib

from dotenv import load_dotenv
from onepasswordconnectsdk.client import Client, new_client
import onepasswordconnectsdk

load_dotenv()

# ⚠️⚠️⚠️
# ! THIS VALUE IS A SECRET. It is the most important secret.
# ! This is the only secret that is not stored in 1Password,
# ! but it's also fine to store in 1PW as well.
# * It's like having access to the vault as if you were in the 1PW UI.
# * They can be configured to have a shelf-life and expire after a given time.
ONEPASSWORD_CONNECT_TOKEN = os.getenv("OP_API_TOKEN")
# ⚠️⚠️⚠️

# if the ONEPASSWORD_CONNECT_TOKEN variable is empty, prompt the user for it
if not ONEPASSWORD_CONNECT_TOKEN:
    ONEPASSWORD_CONNECT_TOKEN = input("Enter your OnePassword Connect API token: ")

# * None of the following values are secrets
ONEPASSWORD_CONNECT_HOST = "https://nothingbut.flowers"
ITEM_NAME = "Secret for SHA"
VAULT_ID = "quvhrzaatbj2wotsjrumx3f62a"  # Discovery day

# * This is how you define the secrets you want to pull out of 1Password
REQUIRED_SECRETS = {
    "sha_input_secret": {
        "opitem": ITEM_NAME,
        "opfield": ".password",
        "opvault": VAULT_ID,
    },
}

# * Open up a client instance to the 1Password Connect API, which is /our/ service.
# * In this case, it's an ECS cluster.
client: Client = new_client(ONEPASSWORD_CONNECT_HOST, ONEPASSWORD_CONNECT_TOKEN)
SECRETS = onepasswordconnectsdk.load_dict(client, REQUIRED_SECRETS)

# write a function named main which requests the user to enter a string with the prompt "Enter the input string"
def main():
    print(
        "We're going to take a string you input and concatenate it with a secret from 1Password and run the result through SHA1."
    )
    user_supplied_string = input("Enter the input string: ")
    print(
        "Resulting SHA1 Hash: ",
        shasum(user_supplied_string, SECRETS["sha_input_secret"]),
    )


# write a function that takes two strings and concatenates them with a hyphen in the middle and computes the shasum
def shasum(s1, s2):
    input = s1 + "-" + s2 + "\n"
    return hashlib.sha1(input.encode("ascii")).hexdigest()


# write the boilerplate code that calls a function named main if this is the main thread
if __name__ == "__main__":
    main()

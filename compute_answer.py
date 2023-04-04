#!/usr/bin/env python3
# import the library needed to do a shasum of a string
import hashlib
import os
from onepasswordconnectsdk.client import Client, new_client

#import library to set environment from .env file
from dotenv import load_dotenv

#load environment variables from .env

load_dotenv()


# ! Important Note: This string is not a secret
VAULT_ID = "quvhrzaatbj2wotsjrumx3f62a" # Discovery day
ITEM_NAME = "Secret for SHA"


TOKEN = os.getenv("OP_API_TOKEN")
# if the TOKEN variable is empty, prompt the user for it
if not TOKEN:
    TOKEN = input("Enter your API token: ")

# write a function named main which requests the user to enter a string with the prompt "Enter the input string"
def main():
    user_supplied_string = input("Enter the input string: ")
    
    # creates a client by supplying hostname and 1Password Connect API token
    client: Client = new_client("https://nothingbut.flowers", TOKEN)




    secret = client.get_item_by_title(f"{ITEM_NAME}", f"{VAULT_ID}")

    #print(secret)
    print(type(secret.fields[0]))

    value = [item for item in secret.fields if item.get('id') == "PASSWORD"]
    print(value)

    print(f"Our secret for '{secret.fields[2].label}' is '{secret.fields[2].value}', 🎉")

    print(shasum(user_supplied_string, secret.fields[2].value))

# write a function that takes two strings and concatenates them with a hyphen in the middle and computes the shasum
def shasum(s1, s2):
    input = s1 + "-" + s2 + "\n"
    return hashlib.sha1(input.encode("ascii")).hexdigest()

# write the boilerplate code that calls a function named main if this is the main thread
if __name__ == "__main__":
    main()
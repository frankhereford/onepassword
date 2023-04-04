#!/usr/bin/env python3
# import the library needed to do a shasum of a string
import hashlib

# write a function named main which requests the user to enter a string with the prompt "Enter the input string"
def main():
    s = input("Enter the input string: ")
    print(shasum(s, s))

# write a function that takes two strings and concatenates them with a hyphen in the middle and computes the shasum
def shasum(s1, s2):
    input = s1 + "-" + s2 + "\n"
    return hashlib.sha1(input.encode("ascii")).hexdigest()

# write the boilerplate code that calls a function named main if this is the main thread
if __name__ == "__main__":
    main()
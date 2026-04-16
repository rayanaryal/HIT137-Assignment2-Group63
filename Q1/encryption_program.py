# -----------------------------------------------------------------------
# HIT137 Assignment 2 - Question 1
# Group: Group 63
# Group Members: Rupesh Timalsina S400656
                 Swastik Bista S400506
                 Rajan Aryal S333047
# Description:
#     This program reads a text file, encrypts its content based on
#     custom shifting rules, decrypts it back, and verifies correctness.
# -----------------------------------------------------------------------


# Function to encrypt single character
def encrypt_char(ch, shift1, shift2):

    if ch.islower():
        if 'a' <= ch <= 'm':
            return chr((ord(ch) - ord('a') + shift1 * shift2) % 26 + ord('a')) + "0"
        else:
            return chr((ord(ch) - ord('a') - (shift1 + shift2)) % 26 + ord('a')) + "1"

    elif ch.isupper():
        if 'A' <= ch <= 'M':
            return chr((ord(ch) - ord('A') - shift1) % 26 + ord('A')) + "0"
        else:
            return chr((ord(ch) - ord('A') + shift2 ** 2) % 26 + ord('A')) + "1"

    else:
        return ch

# Function to decrypt single character
def decrypt_char(pair, shift1, shift2):

    if len(pair) == 1:
        return pair

    ch = pair[0]
    mark = pair[1]

    if ch.islower():
        if mark == "0":
            return chr((ord(ch) - ord('a') - shift1 * shift2) % 26 + ord('a'))
        else:
            return chr((ord(ch) - ord('a') + shift1 + shift2) % 26 + ord('a'))

    elif ch.isupper():
        if mark == "0":
            return chr((ord(ch) - ord('A') + shift1) % 26 + ord('A'))
        else:
            return chr((ord(ch) - ord('A') - shift2 ** 2) % 26 + ord('A'))

    else:
        return ch

# Function to encrypt entire file
def encrypt_file(shift1, shift2):

    try:
        file = open("raw_text.txt", "r")
        content = file.read()
        file.close()

        encrypted = ""

        for ch in content:
            encrypted += encrypt_char(ch, shift1, shift2)

        file = open("encrypted_text.txt", "w")
        file.write(encrypted)
        file.close()

        print("Encryption completed successfully!")

    except FileNotFoundError:
        print("raw_text.txt not found")

# Function to decrypt entire file
def decrypt_file(shift1, shift2):

    try:
        file = open("encrypted_text.txt", "r")
        content = file.read()
        file.close()

        decrypted = ""
        i = 0

        while i < len(content):

            if i + 1 < len(content) and content[i + 1] in "01":
                decrypted += decrypt_char(content[i:i+2], shift1, shift2)
                i += 2
            else:
                decrypted += content[i]
                i += 1

        file = open("decrypted_text.txt", "w")
        file.write(decrypted)
        file.close()

        print("Decryption completed successfully!")

    except FileNotFoundError:
        print("encrypted_text.txt not found")

# Function to verify if original and decrypted files match
def verify_files():

    try:
        file = open("raw_text.txt", "r")
        original = file.read()
        file.close()

        file = open("decrypted_text.txt", "r")
        decrypted = file.read()
        file.close()

        print("Original:", original)
        print("Decrypted:", decrypted)

        if original == decrypted:
            print("Verification SUCCESS: Decrypted text matches original !!")
        else:
            print("Verification FAILED: Decrypted text does NOT match original !!")

    except FileNotFoundError:
        print("missing file for verification")

# -------------------- MAIN PROGRAM ----------------------

def main():

    print("---- Encryption & Decryption Program ----")

    shift1 = int(input("Enter shift 1: "))
    shift2 = int(input("Enter shift 2: "))

    encrypt_file(shift1, shift2)
    decrypt_file(shift1, shift2)
    verify_files()

if __name__ == "__main__":
    main()

'''
HIT137 SOFTWARE NOW
Assignment 2

Group: Group 63
Group Members and Student ID:
        Rupesh Timalsina: S400656
        Swastik Bista: S400506
        Rajan Aryal: S333047
'''


# Function to encrypt single character
def encrypt_char(ch, shift1, shift2):

    if ch.islower():
        # lowercase first half: shift forward
        if 'a' <= ch <= 'm':
            return chr((ord(ch) - ord('a') + shift1 * shift2) % 26 + ord('a')) + "0"
        
        # lowercase second half: shift backward
        else:
            return chr((ord(ch) - ord('a') - (shift1 + shift2)) % 26 + ord('a')) + "1"

    elif ch.isupper():
        # uppercase first half: shift backward
        if 'A' <= ch <= 'M':
            return chr((ord(ch) - ord('A') - shift1) % 26 + ord('A')) + "0"
        
        # uppercase second half: shift forward using shift2 squared
        else:
            return chr((ord(ch) - ord('A') + shift2 ** 2) % 26 + ord('A')) + "1"

    # non-alphabet characters stay same
    else:
        return ch


# Function to decrypt single character
def decrypt_char(pair, shift1, shift2):

    # if not encrypted pair, return as it is
    if len(pair) == 1:
        return pair

    ch = pair[0]
    mark = pair[1]

    if ch.islower():
        # reverse of lowercase first half shift
        if mark == "0":
            return chr((ord(ch) - ord('a') - shift1 * shift2) % 26 + ord('a'))
        
        # reverse of lowercase second half shift
        else:
            return chr((ord(ch) - ord('a') + shift1 + shift2) % 26 + ord('a'))

    elif ch.isupper():
        # reverse of uppercase first half shift
        if mark == "0":
            return chr((ord(ch) - ord('A') + shift1) % 26 + ord('A'))
        
        # reverse of uppercase second half shift
        else:
            return chr((ord(ch) - ord('A') - shift2 ** 2) % 26 + ord('A'))

    # non-alphabet characters stay same
    else:
        return ch


# Function to encrypt entire file
def encrypt_file(shift1, shift2):

    # open original file
    try:
        file = open("raw_text.txt", "r")
        content = file.read()
        file.close()

        encrypted = ""

        # encrypt and save each character
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

    # open encrypted file
    try:
        file = open("encrypted_text.txt", "r")
        content = file.read()
        file.close()

        decrypted = ""
        i = 0

        # read encrypted text and decode using markers and save decrypted file
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

    # read original and decrypted file
    try:
        file = open("raw_text.txt", "r")
        original = file.read()
        file.close()

        file = open("decrypted_text.txt", "r")
        decrypted = file.read()
        file.close()

        print("Original:", original)
        print("Decrypted:", decrypted)

        # compare both files
        if original == decrypted:
            print("Verification SUCCESS: Decrypted text matches original !!")
        else:
            print("Verification FAILED: Decrypted text does NOT match original !!")

    except FileNotFoundError:
        print("missing file for verification")


# -------------------- MAIN PROGRAM ----------------------

def main():

    print("---- Encryption & Decryption Program ----")

    # take shift values from user
    shift1 = int(input("Enter shift 1: "))
    shift2 = int(input("Enter shift 2: "))

    # run encryption, decryption and verification
    encrypt_file(shift1, shift2)
    decrypt_file(shift1, shift2)
    verify_files()


if __name__ == "__main__":
    main()

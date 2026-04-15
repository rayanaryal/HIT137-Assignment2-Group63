# ---------------------------------------------------------------
# HIT137 Assignment 2 - Question 1
# Author: (Your Name)
# Description:
# This program reads a text file, encrypts its content based on
# custom shifting rules, decrypts it back, and verifies correctness.
# ---------------------------------------------------------------

# Function to encrypt a single character based on rules
def encrypt_char(ch, shift1, shift2):
    if ch.islower():
        if 'a' <= ch <= 'm':
            return chr((ord(ch) - ord('a') + (shift1 * shift2)) % 26 + ord('a'))
        else:
            return chr((ord(ch) - ord('a') - (shift1 + shift2)) % 26 + ord('a'))

    elif ch.isupper():
        if 'A' <= ch <= 'M':
            return chr((ord(ch) - ord('A') - shift1) % 26 + ord('A'))
        else:
            return chr((ord(ch) - ord('A') + (shift2 ** 2)) % 26 + ord('A'))

    else:
        return ch


# Function to decrypt a single character (reverse of encryption)
def decrypt_char(ch, shift1, shift2):
    if ch.islower():
        # Apply reverse using SAME condition as encryption
        if 'a' <= ch <= 'm':
            # reverse of forward shift
            return chr((ord(ch) - ord('a') - (shift1 * shift2)) % 26 + ord('a'))
        else:
            # reverse of backward shift
            return chr((ord(ch) - ord('a') + (shift1 + shift2)) % 26 + ord('a'))

    elif ch.isupper():
        if 'A' <= ch <= 'M':
            return chr((ord(ch) - ord('A') + shift1) % 26 + ord('A'))
        else:
            return chr((ord(ch) - ord('A') - (shift2 ** 2)) % 26 + ord('A'))

    else:
        return ch

# Function to encrypt entire file
def encrypt_file(shift1, shift2):
    try:
        # Open raw text file for reading
        with open("raw_text.txt", "r") as file:
            content = file.read()

        encrypted_text = ""

        # Loop through each character and encrypt
        for ch in content:
            encrypted_text += encrypt_char(ch, shift1, shift2)

        # Write encrypted text to new file
        with open("encrypted_text.txt", "w") as file:
            file.write(encrypted_text)

        print("Encryption completed successfully!")

    except FileNotFoundError:
        print("Error: raw_text.txt file not found!")


# Function to decrypt entire file
def decrypt_file(shift1, shift2):
    try:
        # Open encrypted file
        with open("encrypted_text.txt", "r") as file:
            content = file.read()

        decrypted_text = ""

        # Loop through each character and decrypt
        for ch in content:
            decrypted_text += decrypt_char(ch, shift1, shift2)

        # Write decrypted text to file
        with open("decrypted_text.txt", "w") as file:
            file.write(decrypted_text)

        print("Decryption completed successfully!")

    except FileNotFoundError:
        print("Error: encrypted_text.txt file not found!")


# Function to verify if original and decrypted files match
def verify_files():
    try:
        # Read original file
        with open("raw_text.txt", "r") as file:
            original = file.read()

        # Read decrypted file
        with open("decrypted_text.txt", "r") as file:
            decrypted = file.read()

        print("Original:", original)
        print("Decrypted:", decrypted)

        # Compare both contents
        if original == decrypted:
            print("Verification SUCCESS: Decrypted text matches original!")
        else:
            print("Verification FAILED: Decrypted text does NOT match original!")

    except FileNotFoundError:
        print("Error: One or more files missing for verification!")
    


# ---------------- MAIN PROGRAM ----------------

def main():
    print("---- Encryption & Decryption Program ----")

    # Taking user input for shifts
    try:
        shift1 = int(input("Enter value for shift1: "))
        shift2 = int(input("Enter value for shift2: "))
    except ValueError:
        print("Invalid input! Please enter integer values.")
        return

    # Step 1: Encrypt file
    encrypt_file(shift1, shift2)

    # Step 2: Decrypt file
    decrypt_file(shift1, shift2)

    # Step 3: Verify correctness
    verify_files()


# Run the program
if __name__ == "__main__":
    main()
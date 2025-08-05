# Advanced Algorithms Assignment 3 Question 1
# Anthony Medico

# This script is a helper tool I developed to help analyze and crack a substition cipher.
# The goal of this question was to crack the cipher - not necessarily build a polished
# tool, so the code is fairly rough but works for its intended purpose.

# Please see the report.txt document for the full analysis.


ciphertext = "YBLWUDNRRGJXWNGDNRRFYAWHBGBUUWNUYBLWUDNRRGBYGUFNQJDXBGBYLRBIFUWFQNAYHFUBDHJMRJJIFNGUNUGMYGFUHJMENYGFFYBLWUXBGBYLYJUDNRRBYLQNXIYFGGRBDUBYLBYUJUWFGIHMVDXJKUWFWJXBOJYRBIFNCRNEIGMYCFWBYQERJMQEJTFXRBIFGKJIFDXJKNYMYGFFYDBXFNRBYFJDDBXFSMGUCFRJAUWFWJXBOJYCXMGWDBXFJXNCMXYBYLEBUHKNHCFYBLWUDNRRGCFENMGFBUGWFNTHNUWBEIEMXUNBYVMRRFQMVJTFXUWFFHFG"
message_length = len(ciphertext)
letter_count = [0] * 26 # to count frequencies

permutations = dict() # to keep track of guessed substitutions

# count frequency of each letter in cipher text, store in array
for char in ciphertext:
    index = ord(char) - ord('A')
    letter_count[index] += 1

# calculate and print frequencies as a percentage
for i in range(26):
    frequency = (letter_count[i] / message_length) * 100
    if letter_count[i] > 0:
        print(f"{chr(i + ord('A'))} - {frequency:.1f}%", end=', ')
print()

# Function definitions
def print_decrypted_cipher():
    ### Commented out part here displays it on a single line -> worked well on my ultrawide monitor
    # for char in ciphertext:
    #     if char in permutations:
    #         print(permutations[char], end='')
    #     else:
    #         print('-', end='')
    # print()
    # print(ciphertext)
    # print(permutations)

    ### Multiline display: shows 40 characters per line of plaintext followed by ciphertext
    start = 0
    end = 40
    while end <= len(ciphertext):
        print_helper(start, end)
        start += 40
        end += 40
    print_helper(320, len(ciphertext))

# Helps automate printing 40 characters at a time of each plaintext and ciphertext
def print_helper(start, end):
    for i in range(start, end):
        if ciphertext[i] in permutations:
            print(permutations[ciphertext[i]], end='')
        else:
            print('-', end='')
    print()
    print(ciphertext[start:end])

# Implemented after finding the solution, to display solution easily
def solve():
    cipher_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # the solution (correct permutation) used in the substitution cipher
    solution_string = 'wibfcesykomguaz-dljvtphrn-'

    permutations.clear()
    for i in range(26):
        permutations[cipher_chars[i]] = solution_string[i]

# This method will print the key in a readable way
def print_key():
    key = [[], [], [], [], [], [], []]
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, letter in enumerate(letters):
        key[i % 7].append(f"{letter} = {permutations.get(letter)}")

    print("\nKey:")
    for row in key:
        for sub in row:
            print(sub, end="   ")
        print()
    print()

# Running helper tools
# Give user a chance to display cipher/plaintext, add guesses, clear all guesses.
while True:
    choice = input("Options:\n\t1. Print cipher\n\t2. Add substitution\n\t3. Clear substitutions\n\t4. Solve and print.\n\t5. Quit\n")

    if choice == '1':
        print_decrypted_cipher()
    elif choice == '2':
        cipher_char = input("Enter ciphertext letter you've decrypted: ")
        plaintext_char = input("Enter corresponding plaintext char: ")
        if len(cipher_char) != 1 or len(plaintext_char) != 1:
            print("Invalid input")
            continue
        permutations[cipher_char.upper()] = plaintext_char.lower()
    elif choice == '3':
        permutations.clear()
    elif choice == '4':
        solve()
        print_decrypted_cipher()
        print_key()
    elif choice == '5':
        break
    else:
        print("Invalid input. Try again.")


## ROUGH NOTES

# Highest frequency is E (12%)
    # Possible characters: F (10.2%), B (9.3%)

# Next tier: T, A, O, I, N, S, H, R (6-9% each)
#   Possible characters:
#       B (9.3%)
#       Y (8.1%)
#       U (7.5%)
#       N (6.9%)
#       G (6.9%)
#       J (6.3%)
#       R (6.3%)
#       W (5.4%)

# Next tier: D, L (4%)
#   Possible characters:
#       X (5.1%)
#       M (4.2%)
#       D (4.2%)

# Next tier: U, C, M, W, F, G, Y, P, B (1.5-2.8%)
#   Possible characters:
#       M,D (4.2%)
#       H,I,L (2.7%)
#       E (2.4%)
#       C (2.1%)
#       Q (1.8%)
#       K (1.2%)
#       A,T,V (0.9%)

# Last tier: V, K, J, X, Q, Z (< 1%)
#       A,T,V (0.9%)
#       O (0.6%)
#       S (0.3%)
#       P,Z (0%)

# multi-letter repeated sequences:
#   YBLWUDNRRG - 3 times
#   YBLWU - 1 time
#   YGFFY - 2 times
#   UWFWJXBOJY - 2 times

# 2-letter sequences with E (guessing F = E)
#   FN - 5
#   FG - 4
#   FY - 4
#   FU - 3
#   FW - 3
#   FQ, FX, FJ - 2
#   FD, FS, FR, FB, FE - 1

#   WF - 6
#   IF - 5
#   GF, CF - 4
#   XF - 3
#   RF, HF, YF, TF - 2
#   UF - 1

# 3-letter sequences with E as last (guessing F = E)
# THE
#   UWF - 5
#   BIF - 3 (RBIF)
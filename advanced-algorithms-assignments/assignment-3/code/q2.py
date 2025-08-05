# Advanced Algorithms Assignment 3 Question 2
# Anthony Medico

# This script was built in phases where information gained from one phase allowed me to
# then program the second phase, and so on. This is the completed program which correctly
# decrypts a Vigenere Cipher

# Global variables
ciphertext = "CWBTFIRLMJKRWDUIIJUIUICKXVFTHZMGZSIRWDHJQSUEJOXYNWBCIRULNJQJHWFSIKQECPVFPOWFWRWDUIIDXMFSEKQSPVXXAACFFVFASFXYNJBCFVAWPDODHSPOXYNJBXWKQAUCMKNTIFGCJWTULRCCBUGYKEXBVVCHFKYSSUCCMIMAOEWYDNUIIWAUNJSLBBBOHVASOBXTQHFUSFTHJTZFAPBMWNXREJRYJNEMSEPTJNIKQENBROXMFGSVQETPYXQTTPVVBTFELVKYUIIKDMUVQKAEFBRUBTPPHRFHJMIZWTIPYXQTBOHRBIOVJWRSIULFDGIULVBTPPHKQEKBFSNRXPGBFIUIIPNSPGJCJMFDEDNWIJJWUIOHXYAOVHLKQEUVPXNYXPSUJNECYIKLFEEJRTDBQV"
probabilities = [0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020, 0.061, 0.070, 0.002, 0.008, 0.040, 0.024, 0.067, 0.075, 0.019, 0.001, 0.060, 0.063, 0.091, 0.028, 0.010, 0.023, 0.001, 0.020, 0.001]
actual_columns = []  # variable to store columns once m is found

# Function definitions
def calculate_index(columns):
    print("\t", end='')
    for column in columns:
        column = column.strip() # remove the white space added for transposing


        frequencies = [0] * 26 # array to keep character count
        n = len(column) # 'n' from index of coincidence equation
        index_of_coincidence = 0 # initialize result to 0

        # calculate character counts
        # gets ascii value of each char but then subtracts so A = 0, B = 1, etc.
        for char in column:
            index = ord(char) - ord('A')
            frequencies[index] += 1

        # index of coincidence calculation
        for i in range(26):
            index_of_coincidence += (frequencies[i] * (frequencies[i] - 1)) / (n * (n - 1))

        print(f"{index_of_coincidence:.3f}, ", end="")
    print()

def calculate_mutual_index(Y):
    for i, y in enumerate(Y):
        print(f"i = {i + 1}:", end="\t")

        y = y.strip() # remove the added spaces

        frequencies = [0] * 26 # array to keep character count
        n_prime = len(ciphertext) / 6 # we know m=6 now

        # calculate character counts
        for char in y:
            index = ord(char) - ord('A')
            frequencies[index] += 1

        # calculate mutual index of coincidence
        for g in range(26):
            mutual_index = 0 # initialize to 0 for each new g
            for i in range(26):
                mutual_index += (probabilities[i]  * frequencies[(i + g) % 26]) / n_prime

            print(f"{mutual_index:.3f}", end=" ")
        print()


# PROGRAM START
# PHASE 1: Determining m using index of coincidence
for m in range(1, 10): # started out checking 1 - 9, which ended up being enough.
    print(f"m = {m}")

    # divide the text into rows of length m
    m_rows = [ciphertext[i:i + m] for i in range(0, len(ciphertext), m)]

    # make sure the last row is also length m by adding spaces if necessary
    if len(m_rows[-1]) < m:
        m_rows[-1] += ' ' * (m - len(m_rows[-1]))

    # need the rows to be columns instead, can just transpose the matrix to do this
    m_columns = [''.join(row[i] for row in m_rows) for i in range(m)]

    # added the following line once I determined m = 6
    # save the columns to a global variable to be used later with mutual index
    if m == 6:
        actual_columns = list(m_columns)

    for column in m_columns:
        print(f"\t{column}")

    calculate_index(m_columns)


# With the above code, determined that m = 6
# PHASE 2: Calculating mutual index of coincidence
m = 6
print("\nCalculating mutual index:")
calculate_mutual_index(actual_columns)


# From the results above, these indexes had higher index values:
K = [9, 0, 1, 1, 4, 17]
# The keyword is likely JABBER

# PHASE 3: Using the keyword to decipher the text
# Printing out the deciphered text using the key JABBER (9, 0, 1, 1, 4, 17)
print()
print("Plaintext:")
for i in range(len(ciphertext)):
    cipher_char = ciphertext[i] # get each char
    shift_amount = K[i % 6] # get shift amount from keyword
    # get alphabet index of char (A = 0, B = 1, etc.)
    alphabet_index = ord(cipher_char) - ord('A')
    # shift char based on key
    deciphered_char_alphabet_index = (alphabet_index - shift_amount) % 26
    # convert to ascii value (using lower case now)
    deciphered_char_ascii = deciphered_char_alphabet_index + ord('a')
    # use ascii value to get the actual deciphered char
    deciphered_char = chr(deciphered_char_ascii)

    print(deciphered_char, end='')

# PHASE 4: Extreme confusion and then googling and realizing this is a nonsense poem
import itertools, string

def build_passwords():
    chars = string.ascii_lowercase
    attempts = 0
    passwords = []
    for password_length in range(4, 5):
        for guess in itertools.product(chars, repeat=password_length):
            attempts += 1
            guess = ''.join(guess)
            passwords.append(guess)
    return passwords

passwords = build_passwords()
print(passwords)
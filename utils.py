
import random
import string


def generate_account_number():
    # Generate a random string of alphanumeric characters
    random_string = ''.join(random.choices(string.digits, k=2))
    # Combine with a prefix to ensure uniqueness
    account_number = '090' + random_string
    return account_number
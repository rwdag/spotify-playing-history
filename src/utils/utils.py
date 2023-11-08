from random import choices
from string import ascii_letters, digits

def generate_random_string() -> str:
    string = ''.join(choices(ascii_letters + digits, k=32))
    return string
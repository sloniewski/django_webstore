import random
import string


def random_string(n):
    result = ''.join(
        [random.choice(string.ascii_letters + string.digits) for x in range(n)])
    return result

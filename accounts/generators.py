import random

def generate_10_digit_number_starting_with_2():
    # Start with '2' and add 9 random digits
    return int("2" + "".join(str(random.randint(0, 9)) for _ in range(9)))


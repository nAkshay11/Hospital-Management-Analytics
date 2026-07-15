def positive_number(value):
    return value >= 0


def valid_rating(value):
    return 1 <= value <= 5


def valid_email(email):
    return "@" in email


def valid_phone(phone):
    return len(phone) == 10
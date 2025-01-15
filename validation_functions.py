def validate_decimal_input(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def validate_numeric_input(value):
    return value.isdigit()

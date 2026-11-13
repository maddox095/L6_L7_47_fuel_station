from math import isfinite
from statistics import mean


def _nonnegative_number(text):
    try:
        value = float(text)
    except ValueError:
        return None
    if not isfinite(value) or value < 0:
        return None
    return value


def parse_purchase(text):
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    grade = parts[0].strip().title()
    litres = _nonnegative_number(parts[1])
    if not grade or litres is None:
        return None
    return grade, litres


def volume_average(volumes_csv):
    if not isinstance(volumes_csv, str):
        return None
    values = [_nonnegative_number(item) for item in volumes_csv.split(',')]
    if any(value is None for value in values):
        return None
    # mean also handles large finite volumes without overflowing their sum.
    return mean(values)


def payable_bill(text):
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    bill = _nonnegative_number(parts[0])
    discount = _nonnegative_number(parts[1])
    if bill is None or discount is None:
        return None
    total = bill * 1.18 - discount
    if not isfinite(total):
        return None
    return max(total, 0.0)


def main():
    print("==== Running parse_purchase ====")
    text = input("Enter grade:litres (e.g. diesel:25): ")
    result = parse_purchase(text)
    print("Invalid purchase" if result is None else f"Grade and Litres: {result}")

    print("\n==== Running volume_average ====")
    text = input("Enter pump volumes in litres as CSV (e.g. 10,25,40): ")
    result = volume_average(text)
    print("Invalid volumes" if result is None else f"Average Volume: {result}")

    print("\n==== Running payable_bill ====")
    text = input("Enter bill|discount (e.g. 2500|100): ")
    result = payable_bill(text)
    print("Invalid bill" if result is None else f"Payable Bill: {result}")


if __name__ == "__main__":
    main()

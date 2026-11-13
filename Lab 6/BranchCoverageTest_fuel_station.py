import pytest

from fuel_station import fuel_bill, pump_allowed, session_status


def test_unknown_grade():
    with pytest.raises(ValueError, match='unknown fuel grade'):
        fuel_bill('petrol', 10, 'silver')


def test_known_grade():
    assert fuel_bill('premium', 15, 'silver') == 0


def test_negative_litres():
    with pytest.raises(ValueError, match='invalid litres'):
        fuel_bill('regular', -1, 'silver')


def test_zero_litres():
    assert fuel_bill('regular', 0, 'silver') == 0


def test_non_gold_no_bonus():
    assert fuel_bill('regular', 20, 'silver') == 1050


def test_gold_gets_bonus():
    assert fuel_bill('regular', 20, 'gold') == 525


def test_gold_diesel_has_no_bonus():
    assert fuel_bill('diesel', 30, 'gold') == 900


def test_exactly_covered_litres():
    assert fuel_bill('regular', 10, 'silver') == 0


def test_one_extra_litre():
    assert fuel_bill('regular', 11, 'silver') == 105


def test_premium_rate():
    assert fuel_bill('premium', 25, 'silver') == 1050


def test_diesel_rate():
    assert fuel_bill('diesel', 30, 'silver') == 900


def test_extra_exactly_30_no_bulk_discount():
    assert fuel_bill('regular', 40, 'silver') == 3150


def test_extra_31_bulk_discount():
    assert fuel_bill('regular', 41, 'silver') == 3069


def test_extra_31_bulk_gold_discount():
    # Gold covers 15 litres: 46 - 15 = 31 extra, rate 95.
    assert fuel_bill('regular', 46, 'gold') == 2945


def test_bulk_diesel_silver():
    assert fuel_bill('diesel', 51, 'silver') == 2604


def test_bulk_diesel_gold():
    # Diesel gets no extra voucher litres; its bulk gold rate is 80.
    assert fuel_bill('diesel', 51, 'gold') == 2480


def test_fleet_at_limit():
    assert pump_allowed(200, 3, True) is True


def test_fleet_over_limit():
    assert pump_allowed(201, 1, True) is False


def test_fleet_ignores_containers():
    assert pump_allowed(10, 9, True) is True


def test_nonfleet_over_litres_limit():
    assert pump_allowed(61, 0, False) is False


def test_nonfleet_at_litres_limit():
    assert pump_allowed(60, 1, False) is True


def test_nonfleet_one_container():
    assert pump_allowed(30, 1, False) is True


def test_nonfleet_too_many_containers():
    assert pump_allowed(30, 2, False) is False


@pytest.mark.parametrize('is_card_payment,is_night,cutoff', [
    (False, False, 30),
    (True, False, 60),
    (False, True, 60),
    (True, True, 90),
], ids=['cash-day', 'card-day', 'cash-night', 'card-night'])
@pytest.mark.parametrize('offset,expected', [
    (0, 'active'),
    (-1, 'warning'),
    (-15, 'warning'),
    (-16, 'timed_out'),
], ids=['at-cutoff', 'warning-upper', 'warning-lower', 'timed-out'])
def test_session_boundaries(is_card_payment, is_night, cutoff, offset, expected):
    assert session_status(cutoff + offset, is_card_payment, is_night) == expected

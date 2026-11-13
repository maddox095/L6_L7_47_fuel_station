import pytest

from fuel_station import fuel_bill, pump_allowed, session_status


def test_within_covered_litres():
    assert fuel_bill('regular', 8, 'silver') == 0


def test_unknown_grade():
    with pytest.raises(ValueError, match='unknown fuel grade'):
        fuel_bill('petrol', 10, 'silver')


def test_negative_litres():
    with pytest.raises(ValueError, match='invalid litres'):
        fuel_bill('regular', -1, 'silver')


def test_gold_bonus():
    # 15 litres covered, so 10 extra litres at 105.
    assert fuel_bill('regular', 25, 'gold') == 1050


def test_regular_rate():
    assert fuel_bill('regular', 20, 'silver') == 1050


def test_diesel_rate():
    assert fuel_bill('diesel', 30, 'silver') == 900


def test_bulk_discount():
    # 40 extra litres at 105 - 6.
    assert fuel_bill('regular', 50, 'silver') == 3960


def test_bulk_gold_discount():
    # 40 extra litres at 105 - 6 - 4.
    assert fuel_bill('regular', 55, 'gold') == 3800


def test_normal_pump_request():
    assert pump_allowed(30, 1, False) is True


def test_fleet_request():
    assert pump_allowed(150, 2, True) is True


def test_nonfleet_over_limit():
    assert pump_allowed(61, 0, False) is False


def test_active_session():
    assert session_status(30, False, False) == 'active'


def test_warning_session():
    assert session_status(20, False, False) == 'warning'


def test_timed_out_session():
    assert session_status(14, False, False) == 'timed_out'


def test_card_payment_at_night():
    assert session_status(90, True, True) == 'active'

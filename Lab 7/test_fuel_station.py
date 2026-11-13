from math import isfinite

import pytest
from hypothesis import given, settings, strategies as st

from fuel_station import parse_purchase, volume_average, payable_bill


@settings(max_examples=500, report_multiple_bugs=False)
@given(st.text() | st.none())
def test_parse_purchase_no_crash(s):
    result = parse_purchase(s)
    if result is not None:
        grade, litres = result
        assert grade and grade == grade.strip().title()
        assert isfinite(litres) and litres >= 0


@settings(max_examples=500, report_multiple_bugs=False)
@given(st.text() | st.none())
def test_volume_average_no_crash(s):
    result = volume_average(s)
    assert result is None or (isfinite(result) and result >= 0)


@settings(max_examples=500, report_multiple_bugs=False)
@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    result = payable_bill(s)
    assert result is None or (isfinite(result) and result >= 0)


@settings(max_examples=200)
@given(st.sampled_from(['regular', 'premium', 'diesel']),
       st.floats(min_value=0, max_value=1e6, allow_nan=False))
def test_valid_purchase(grade, litres):
    assert parse_purchase(f'  {grade.upper()} : {litres} ') == (grade.title(), litres)


@settings(max_examples=200)
@given(st.lists(st.integers(min_value=0, max_value=1000000), min_size=1, max_size=30))
def test_valid_average(values):
    result = volume_average(','.join(str(value) for value in values))
    assert result == pytest.approx(sum(values) / len(values))
    assert min(values) <= result <= max(values)


@settings(max_examples=200)
@given(st.integers(min_value=0, max_value=1000000),
       st.integers(min_value=0, max_value=2000000))
def test_valid_bill(bill, discount):
    # Integer paise calculation is an independent check of the tax formula.
    expected = max(bill * 118 - discount * 100, 0) / 100
    assert payable_bill(f'{bill}|{discount}') == pytest.approx(expected, abs=1e-8)


@settings(max_examples=200)
@given(st.lists(st.floats(min_value=0, max_value=1e308, allow_nan=False),
                min_size=1, max_size=20))
def test_average_of_large_finite_values(values):
    result = volume_average(','.join(map(str, values)))
    assert isfinite(result)
    assert min(values) <= result <= max(values)


@given(st.one_of(st.integers(), st.floats(), st.booleans(), st.binary(),
                 st.lists(st.integers()), st.dictionaries(st.text(), st.integers())))
def test_other_input_types_are_rejected(value):
    assert parse_purchase(value) is None
    assert volume_average(value) is None
    assert payable_bill(value) is None


@pytest.mark.parametrize('text', [
    None, '', 'diesel', 'diesel:1:2', ':25', '  :25', 'diesel:',
    'diesel:abc', 'diesel:-1', 'diesel:nan', 'diesel:inf',
    'diesel:-inf', 'diesel:1e309',
])
def test_bad_purchase(text):
    assert parse_purchase(text) is None


@pytest.mark.parametrize('text', [
    None, '', ' ', '10,,20', '10,', ',10', 'one,two', '10,-1',
    'nan,2', 'inf,2', '-inf,2', '1e309,2',
])
def test_bad_volumes(text):
    assert volume_average(text) is None


@pytest.mark.parametrize('text', [
    None, '', '100', '100|1|2', '|10', '100|', 'abc|10', '100|abc',
    '-100|10', '100|-10', 'nan|0', '100|nan', 'inf|0', '100|inf',
    '-inf|0', '1e309|0', '1.7e308|0',
])
def test_bad_bill(text):
    assert payable_bill(text) is None


def test_normal_inputs_and_boundaries():
    assert parse_purchase(' diesel : 25.5 ') == ('Diesel', 25.5)
    assert parse_purchase('regular:0') == ('Regular', 0.0)
    assert volume_average('10,25,40') == 25.0
    assert volume_average('10,11') == 10.5
    assert volume_average(' 1.5, 2.5 ') == 2.0
    assert volume_average('0') == 0.0
    assert volume_average('1e308,1e308') == 1e308
    assert payable_bill('2500|100') == 2850.0
    assert payable_bill('100|200') == 0.0
    assert payable_bill('0|0') == 0.0
    assert payable_bill(' 100.5 | 10.25 ') == pytest.approx(108.34)

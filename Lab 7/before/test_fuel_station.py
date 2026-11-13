from hypothesis import given, settings, strategies as st
from fuel_station import parse_purchase, volume_average, payable_bill


@settings(max_examples=500, report_multiple_bugs=False)
@given(st.text() | st.none())
def test_parse_purchase_no_crash(s):
    parse_purchase(s)


@settings(max_examples=500, report_multiple_bugs=False)
@given(st.text() | st.none())
def test_volume_average_no_crash(s):
    volume_average(s)


@settings(max_examples=500, report_multiple_bugs=False)
@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    payable_bill(s)

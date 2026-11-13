# Lab 6 - Code and Branch Coverage

Vishwas Gowda S

PES1UG24CS539

Assignment 47 - Fuel Station

The supplied fuel_station.py is unchanged. It calculates fuel bills, checks
pump requests and gives the payment session status.

## Files

- CodeCoverageTest_fuel_station.py - 15 tests for statement coverage.
- BranchCoverageTest_fuel_station.py - 39 tests for branches and boundaries.
- test_fuel_station.py - the two supplied starter tests.
- code_coverage.png and branch_coverage.png - result screenshots.
- code_coverage.txt and branch_coverage.txt - the saved command output.

## Run

Tested with Python 3.12.12. From the Lab 6 folder:

```text
python -m pip install -r requirements.txt
```

Code coverage:

```text
python -m coverage run --source=fuel_station --data-file=.coverage.code -m pytest CodeCoverageTest_fuel_station.py
python -m coverage report --data-file=.coverage.code -m --fail-under=100
```

Branch coverage:

```text
python -m coverage run --branch --source=fuel_station --data-file=.coverage.branch -m pytest BranchCoverageTest_fuel_station.py
python -m coverage report --data-file=.coverage.branch -m --fail-under=100
```

All tests:

```text
python -m pytest -q
```

pytest.ini includes the two coverage test filenames in normal test discovery.
The two runs use separate coverage data files so the results do not overwrite
each other. Only fuel_station.py is measured, not the test files.

## Results

| Suite | Passed | Statements | Missed | Branches | Partial | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Code coverage | 15 | 37 | 0 | Not measured | Not measured | 100% |
| Branch coverage | 39 | 37 | 0 | 26 | 0 | 100% |

All three test files together: 56 passed.

The branch tests check invalid grades and negative litres, all three grades,
gold and non-gold customers, exact voucher limits, and 30 versus 31 extra
litres. Gold diesel gets no bonus litres, but does get the extra bulk rate
reduction. The reduced rate applies to all extra litres once extra exceeds 30.

Pump tests cover the 200/201 fleet limit, the 60/61 normal limit and the
1/2 container boundary. Fleet requests ignore the container count in the
supplied code, so that behaviour is tested too.

Session tests check the active cutoff, both ends of the warning interval and
the first timed-out value for all four card/cash and day/night combinations.

The screenshots show the saved command output in a dark viewer.
100% measured coverage does not prove that the program is
correct for every possible input or that every combination of paths was tested.

# Lab 7 - Fuzz testing

Vishwas Gowda S

PES1UG24CS539

Assignment: https://github.com/SETAPESU26/L6_L7_47_fuel_station/tree/main/Lab%207
Starter commit: db539ffb0412cf72275c584357ed4c4451f479fc

The handout uses processor.py as an example filename. This assignment has
fuel_station.py, so the same steps are done on that file.

## Run

Tested with Python 3.12.12. From this folder:

```text
python -m pip install -r requirements.txt
python fuel_station.py
python -m pytest test_fuel_station.py -q --hypothesis-seed=47
```

## What changed

- All three functions return None for invalid input. The console prints an
  error message and moves to the next prompt.
- Check the input type before splitting. Check the number of fields too.
- Reject missing values, invalid numbers, negatives, NaN and infinity.
- Reject blank fuel grades. Lab 7 does not specify a fixed list of grades,
  so other non-empty grade names are still accepted and title-cased.
- volume_average uses a real mean instead of integer division. For example,
  10,11 now gives 10.5. Decimal volumes work too. statistics.mean avoids
  overflowing the sum for inputs such as 1e308,1e308.
- The bill still adds 18% tax, subtracts the discount and clamps the result
  to zero. If the calculation overflows, it returns None. This exercise uses
  floating point numbers as in the starter; currency rounding was not added.

Zero values and surrounding whitespace are valid. A bad CSV item rejects
the whole list instead of silently skipping it.

## Tests and evidence

The three starter no-crash tests use st.text() | st.none(), with up to 500
examples each. More properties generate valid purchases, lists of volumes,
bills and non-string inputs. Named regression cases cover the edge cases.
The valid-input tests also check answers, so returning None for everything
would fail the suite.

Before: 3 failed. Hypothesis found None for each function; the original code
calls split() without checking its type. The original interactive run also
shows truncation (10 instead of 10.5) and a missing-delimiter crash.

After: 51 passed. The count is pytest test cases, not the number of generated
inputs. Fuzzing gives evidence for the tested inputs, not proof for all inputs.

- PES1UG24CS539_Lab7.pdf contains the four required output screenshots and notes.
- evidence/ contains the screenshots and the actual stdout/stderr transcripts.
  Screenshots show those transcripts in a dark output viewer with the browser
  header included. Inputs and exit codes are included in the captures.
- before/fuel_station.py is the unchanged supplied application.
- before/test_fuel_station.py contains the completed starter fuzz tests.

To reproduce the failures (these are supposed to fail):

```text
cd before
python fuel_station.py
python -m pytest test_fuel_station.py -q --tb=short --hypothesis-seed=47
```

Run the final tests from the Lab 7 folder. pytest.ini excludes before/ from normal test
discovery, so the intentionally failing baseline is not collected.

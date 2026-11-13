# Fuel Station - Labs 6 and 7

Vishwas Gowda S

PES1UG24CS539

Fork of [assignment 47](https://github.com/SETAPESU26/L6_L7_47_fuel_station).
The [SE labs repository](https://github.com/maddox095/SE-Labs-PES1UG24CS539)
also keeps copies of both submissions.

- [Lab 6](Lab%206/README.md): separate code and branch coverage suites.
  56 tests pass; the application has 37/37 statements and 26/26 branches covered.
- [Lab 7](Lab%207/README.md): input validation fixes, Hypothesis tests,
  regression cases, screenshots and the PDF report. 51 tests pass.

## Run

Use Python 3.12. Run each lab from its own folder because both contain a
module named fuel_station.py.

```text
cd "Lab 6"
python -m pip install -r requirements.txt
python -m pytest -q
```

For the coverage commands, see the Lab 6 README.

From the repository root, run Lab 7 with:

```text
cd "Lab 7"
python -m pip install -r requirements.txt
python -m pytest -q --hypothesis-seed=47
```

The screenshots and saved output were recorded in the SE labs checkout.
The same application and test files were checked again in this fork.
Lab 7's before/ folder preserves the original application and its expected
failing fuzz tests; it is excluded from normal test discovery.

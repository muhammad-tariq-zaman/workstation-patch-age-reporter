# workstation-patch-age-reporter

Report days since each workstation was last patched from a CSV: OVERDUE over 30 days, DUE SOON at 15–30 days, OK within 14 days — oldest patch first.

## How to run

```sh
python3 main.py patches.csv --as-of 2026-11-07
```

## Example output

```
PC-12: OVERDUE (last patched 2026-10-01, 37 days ago)
PC-07: OK (last patched 2026-11-01, 6 days ago)
1 overdue, 0 due soon.
```

Standard library only. Run the tests with `python3 -m unittest discover`.

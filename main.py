"""Report days since each workstation was last patched.

Usage: python3 main.py patches.csv [--as-of 2026-11-07]
CSV columns: host,last_patch_date (ISO, e.g. 2026-10-20).
OVERDUE: patched more than 30 days ago. DUE SOON: 15-30 days.
OK: patched within the last 14 days. Oldest patch first.
"""
import argparse, csv, sys
from datetime import date

OVERDUE_DAYS = 30
DUE_SOON_DAYS = 15

def report(rows, as_of=None):
    as_of = as_of or date.today()
    out = []
    for row in rows:
        last = date.fromisoformat(row["last_patch_date"].strip())
        age = (as_of - last).days
        if age > OVERDUE_DAYS:
            verdict = "OVERDUE"
        elif age >= DUE_SOON_DAYS:
            verdict = "DUE SOON"
        else:
            verdict = "OK"
        out.append((row["host"].strip(), last.isoformat(), age, verdict))
    return sorted(out, key=lambda r: -r[2])

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--as-of", default=None, help="reference date YYYY-MM-DD (default: today)")
    args = parser.parse_args(argv)
    as_of = date.fromisoformat(args.as_of) if args.as_of else None
    with open(args.path, newline="", encoding="utf-8") as f:
        results = report(list(csv.DictReader(f)), as_of)
    for host, last, age, verdict in results:
        print(f"{host}: {verdict} (last patched {last}, {age} days ago)")
    print(f"{sum(1 for *_, v in results if v == 'OVERDUE')} overdue, "
          f"{sum(1 for *_, v in results if v == 'DUE SOON')} due soon.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

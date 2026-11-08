import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import report

import datetime
AS_OF = datetime.date(2026, 11, 7)

def row(h, d):
    return {"host": h, "last_patch_date": d}

class TestPatchAge(unittest.TestCase):
    def test_overdue(self):
        self.assertEqual(report([row("PC-1", "2026-10-01")], AS_OF)[0][3], "OVERDUE")
    def test_due_soon(self):
        self.assertEqual(report([row("PC-1", "2026-10-20")], AS_OF)[0][3], "DUE SOON")
    def test_ok(self):
        self.assertEqual(report([row("PC-1", "2026-11-01")], AS_OF)[0][3], "OK")
    def test_exactly_30_days_due_soon(self):
        self.assertEqual(report([row("PC-1", "2026-10-08")], AS_OF)[0][3], "DUE SOON")
    def test_exactly_31_days_overdue(self):
        self.assertEqual(report([row("PC-1", "2026-10-07")], AS_OF)[0][3], "OVERDUE")
    def test_age_days_computed(self):
        self.assertEqual(report([row("PC-1", "2026-10-01")], AS_OF)[0][2], 37)
    def test_oldest_first(self):
        r = report([row("A", "2026-11-01"), row("B", "2026-10-01")], AS_OF)
        self.assertEqual(r[0][0], "B")

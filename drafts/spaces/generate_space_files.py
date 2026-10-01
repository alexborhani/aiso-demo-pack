#!/usr/bin/env python3
"""
Build the files a presenter uploads into a person's space (DEMOS.md scenario 37): a Word file carrying the
Purview label "Confidential" (the same fictional tenant and label ids as the labelled-files store), a plain
Markdown note with no label, and a sensor log too large for a space.

    python3 -m venv .venv && .venv/bin/pip install python-docx openpyxl python-pptx pypdf reportlab
    .venv/bin/python drafts/spaces/generate_space_files.py [--out data/space-files]

Deterministic: the same files on every run.
"""
from __future__ import annotations

import argparse
import os
import random
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "classification"))
from generate_labelled_files import label_office, make_docx  # noqa: E402

TRIPS = [
    "Between 1 and 26 September 2026 the guard interlock on the Riverside test rig tripped 41 times over 19 shifts, about twice a shift. Each trip stops the pump under test and costs 20 to 30 minutes of rig time.",
    "Causes, from the rig book and the controller's event log: 29 trips came from guard door sensor GS-2 on the rear guard door; 8 came from operators opening the front guard during a run; 4 came from the PLC watchdog after the controller firmware was updated to 4.2 on 15 September.",
    "GS-2: the sensor bracket on the rear guard door is cracked at the weld. The closed door sags about 3 mm, and above 1,500 rpm the rig's vibration moves the magnet past the sensor's 5 mm switching distance. The sensor itself tested good on the bench.",
    "Recommendation 1: replace the bracket and fit a coded magnetic safety sensor (Sentrel CMS-40) in place of GS-2. Sentrel Automation quoted 3,400 pounds including fitting, valid until 31 October 2026. Adding a software debounce to the safety channel was considered and rejected by the safety review: a trip on the safety channel must never be delayed.",
    "Recommendation 2: operator trips. Re-brief the rig team on the start-up checklist and fit a 'run in progress' beacon above the front guard (quoted at 620 pounds).",
    "Recommendation 3: watchdog trips. Firmware 4.2 lengthened the controller's scan cycle. Raise it with the controls team before the Halden rigs take the same update.",
    "Owner: Sam Reyes, automation engineering. Review with the Riverside service manager on 9 October 2026.",
]

NOTES = """# My working notes: Riverside rig trips

- Tuesday: check the torque on the GS-2 bracket bolts before the bracket comes off.
- Ask Halden whether their rigs tripped after firmware 4.2 (they have not taken it yet, I think).
- Rig book: 22 to 24 September entries are missing pump serials. Ask the night shift.
- Keep the old GS-2 sensor for the bench test record.
"""


def sensor_log(rows: int = 2900) -> str:
    rnd = random.Random(2026)
    t = datetime(2026, 1, 5, 6, 0)
    out = ["timestamp,site,rig,pump_serial,rpm,vibration_mm_s,bearing_temp_c,discharge_bar,trip"]
    for i in range(rows):
        rpm = rnd.choice([900, 1200, 1500, 1800, 2100])
        vib = round(1.2 + rpm / 1000 + rnd.random() * 1.6, 2)
        temp = round(38 + rpm / 120 + rnd.random() * 6, 1)
        bar = round(2.0 + rpm / 900 + rnd.random() * 0.8, 2)
        trip = "guard" if rpm >= 1500 and rnd.random() < 0.03 else ""
        out.append(f"{t:%Y-%m-%dT%H:%M},Halden,HR-{1 + i % 3},MW300-{4100 + (i // 12) % 300:04d},{rpm},{vib},{temp},{bar},{trip}")
        t += timedelta(minutes=110)
    return "\n".join(out) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "space-files"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    files = {
        "riverside-interlock-trips.docx": label_office(make_docx("Riverside test rig: guard interlock trips, September 2026", TRIPS), "Confidential"),
        "rig-trip-working-notes.md": NOTES.encode(),
        "halden-rig-sensor-log-2026.csv": sensor_log().encode(),
    }
    for name, data in files.items():
        with open(os.path.join(a.out, name), "wb") as f:
            f.write(data)
        print(f"{name}: {len(data):,} bytes")


if __name__ == "__main__":
    main()

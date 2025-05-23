# run pip install sickle

from zbsickle.app import ZbPreviewSickle
from zbsickle.models import ZbPreviewRecord
import time
import csv


def log(m):
    print(m)


def run(
    max_records=10,
    outfile="out.csv",
    log_interval=1000,
    only_complete=True,
    fieldnames=ZbPreviewRecord.fieldnames,
):
    t0 = time.time()
    s = ZbPreviewSickle()
    r = s.ListRecords()
    i = 0
    w: csv.DictWriter
    with open(outfile, "w") as csvfile:
        w = csv.DictWriter(csvfile, fieldnames)
        w.writeheader()
        for row in r:
            row.fieldnames = fieldnames
            added = row.writerow(w, only_complete)
            if max_records > 0 and i > max_records:
                return
            elif added:
                i += 1
            if i % log_interval == 0:
                current_time = time.time()
                log(f"{i / (current_time - t0)} records per second")


if __name__ == "__main__":
    run(0, "out.csv", 1000, False)

import csv
import os
from datetime import datetime
import requests

SHEET_URL = "https://docs.google.com/spreadsheets/d/1T0IEMCT2evUNUncni6cSqms-YqDVSaIcmtc3_cRuxLs/export?format=csv&gid=0"
FILENAME = "licensing_applications.csv"

response = requests.get(SHEET_URL)
response.raise_for_status()
header, *rows = csv.reader(response.text.splitlines(keepends=True))

existing = []
if os.path.exists(FILENAME):
    with open(FILENAME, newline="") as f:
        existing = list(csv.reader(f))[1:]

for row in rows:
    if row not in existing:
        existing.append(row)

existing.sort(key=lambda row: datetime.strptime(row[0], "%d/%m/%Y"))

with open(FILENAME, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(existing)

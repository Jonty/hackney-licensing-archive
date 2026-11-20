import csv
import os
from datetime import datetime
import requests

SHEET_URL = "https://docs.google.com/spreadsheets/d/1fIm5OBC26yXWvCi5n2exUtm22bcl9NQXhgkD-0SvogQ/export?format=csv&gid=0"
FILENAME = "licensing_applications.csv"
DATE_COLUMN = "Date Received"
# We allow these columns to update an existing row rather than adding a new one
MUTABLE_COLUMNS = {"Status"}

response = requests.get(SHEET_URL)
response.raise_for_status()
response.encoding = "utf-8"
header, *rows = csv.reader(response.text.splitlines(keepends=True))
rows = [row for row in rows if any(cell.strip() for cell in row)]

existing = []
if os.path.exists(FILENAME):
    with open(FILENAME, newline="") as f:
        existing_header, *existing = csv.reader(f)
    if existing_header != header:
        raise SystemExit(
            f"Spreadsheet columns have changed.\n"
            f"  archive: {existing_header}\n"
            f"  sheet:   {header}"
        )

key_indexes = [i for i, name in enumerate(header) if name not in MUTABLE_COLUMNS]


def key(row):
    return tuple(row[i] for i in key_indexes)


archive = {key(row): row for row in existing}
for row in rows:
    archive[key(row)] = row

date_index = header.index(DATE_COLUMN)
merged = sorted(
    archive.values(),
    key=lambda row: datetime.strptime(row[date_index].strip(), "%d/%m/%Y"),
)

with open(FILENAME, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(merged)

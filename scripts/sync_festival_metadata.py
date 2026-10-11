"""Regenerate the festival-icons metadata.jsonl from labels.csv and validate PNG paths."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "cases" / "festival-icons"
with (ROOT / "labels.csv").open(encoding="utf-8-sig", newline="") as f:
    records = list(csv.DictReader(f))
paths = [r["image"] for r in records]
if len(set(paths)) != len(paths):
    raise ValueError("Duplicate image labels")
actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "images").glob("*.png")}
if set(paths) != actual:
    raise ValueError(f"Missing images: {sorted(set(paths)-actual)}; unlabelled: {sorted(actual-set(paths))}")
for record in records:
    if not record["caption"]:
        raise ValueError(f"Empty caption for {record['image']}")
with (ROOT / "metadata.jsonl").open("w", encoding="utf-8", newline="\n") as f:
    for r in records:
        f.write(json.dumps({"file_name": r["image"], "text": r["caption"]}, ensure_ascii=False) + "\n")
print(f"Validated and generated metadata for {len(records)} images.")

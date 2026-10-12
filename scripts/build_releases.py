"""Validate a case and create a reproducible GitHub Release ZIP (Python stdlib)."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from zipfile import ZIP_STORED, ZipFile, ZipInfo

CASE_PREFIX = {"tomato-leaves": "tomato", "festival-icons": "festival"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def validate_case(case_dir: Path, case_id: str, tag: str) -> dict:
    prefix = CASE_PREFIX[case_id]
    match = re.fullmatch(rf"{prefix}-v(\d+\.\d+\.\d+)", tag)
    if not match:
        raise ValueError(f"Unexpected tag for {case_id}: {tag}")
    required = [case_dir / name for name in ("manifest.json", "labels.csv", "metadata.jsonl", "README.md")]
    if not all(file.is_file() for file in required):
        raise ValueError("Missing metadata or README")
    manifest = json.loads((case_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("case_id") != case_id or manifest.get("version") != "v" + match.group(1):
        raise ValueError("Manifest case/version differs from tag")
    with (case_dir / "labels.csv").open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columns = {"image", "label", "split"} if case_id == "tomato-leaves" else {"image", "caption"}
        if not columns <= set(reader.fieldnames or []):
            raise ValueError("Unexpected labels.csv columns")
        rows = list(reader)
    if not rows or len(rows) != manifest.get("image_count"):
        raise ValueError("Wrong label/manifest image count")
    image_names = set()
    expected_metadata = {}
    for row in rows:
        rel = PurePosixPath(row["image"])
        if (not rel.parts or rel.parts[0] != "images" or rel.is_absolute() or
                ".." in rel.parts or "\\" in row["image"] or rel.suffix.lower() not in IMAGE_EXTENSIONS):
            raise ValueError(f"Invalid image path: {row['image']}")
        if row["image"] in image_names:
            raise ValueError(f"Duplicate image: {row['image']}")
        image_names.add(row["image"])
        if case_id == "tomato-leaves":
            if row["split"] not in {"train", "test"} or row["label"] not in manifest["classes"]:
                raise ValueError(f"Invalid label/split: {row}")
            if rel.parts[:3] != ("images", row["split"], row["label"]):
                raise ValueError(f"Path differs from label/split: {row}")
            expected_metadata[row["image"]] = {"label": row["label"], "split": row["split"]}
        else:
            if not row["caption"].strip():
                raise ValueError(f"Empty caption: {row}")
            expected_metadata[row["image"]] = {"text": row["caption"]}
    actual_images = {}
    for p in (case_dir / "images").rglob("*"):
        if p.is_symlink():
            raise ValueError(f"Symlink in images: {p}")
        if p.is_file():
            if p.suffix.lower() not in IMAGE_EXTENSIONS or p.stat().st_size == 0:
                raise ValueError(f"Unexpected or empty image: {p}")
            actual_images[p.relative_to(case_dir).as_posix()] = p
    if image_names != set(actual_images):
        raise ValueError("Images and labels.csv do not agree")
    metadata = {}
    for line in (case_dir / "metadata.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            name = item["file_name"]
            if name in metadata:
                raise ValueError("Duplicate metadata file_name")
            metadata[name] = ({"label": item["label"], "split": item["split"]}
                              if case_id == "tomato-leaves" else {"text": item["text"]})
    if metadata != expected_metadata:
        raise ValueError("metadata.jsonl and labels.csv do not agree")
    for p in case_dir.rglob("*"):
        if p.is_symlink():
            raise ValueError(f"Symlink not allowed in release: {p}")
    return manifest

def build_release(repo_root: Path, case_id: str, tag: str, output_dir: Path):
    case_dir = repo_root / "cases" / case_id
    manifest = validate_case(case_dir, case_id, tag)
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{case_id}.zip"
    with ZipFile(archive, "w", compression=ZIP_STORED, allowZip64=True) as z:
        for file in sorted(p for p in case_dir.rglob("*") if p.is_file()):
            name = f"{case_id}/{file.relative_to(case_dir).as_posix()}"
            info = ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, file.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = output_dir / (archive.name + ".sha256")
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="ascii")
    print(f"{case_id}: {manifest['image_count']} images, {archive.stat().st_size} bytes, sha256={digest}")
    return archive, checksum

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--case", choices=sorted(CASE_PREFIX), required=True)
    p.add_argument("--tag", required=True)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    build_release(args.root, args.case, args.tag, args.out or (args.root / "dist"))

if __name__ == "__main__":
    main()

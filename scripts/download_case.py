"""Fetch one dataset case from a public GitHub repo (no Release required).

Python 3.9+ standard library only.
Example:
    data_dir = download_case("festival-icons", revision="main", dest="/content/sample_data")
For repeatable lessons, pin revision to a commit SHA or an immutable tag.
"""
import base64
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO = "708san/CV_sample_data"
KNOWN_CASES = {"festival-icons", "tomato-leaves"}
_SAFE_ID = re.compile(r"^[a-zA-Z0-9_-]+$")
_SAFE_REF = re.compile(r"^[a-zA-Z0-9._/-]+$")


def _read(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "CV-sample-data-Colab"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def download_case(case_id: str, revision: str = "main", dest: str = "sample_data",
                  workers: int = 8) -> Path:
    """Download only files under cases/<case_id>/ and validate image/metadata consistency."""
    if case_id not in KNOWN_CASES or not _SAFE_ID.fullmatch(case_id):
        raise ValueError(f"Unknown case: {case_id}")
    if not _SAFE_REF.fullmatch(revision) or ".." in revision or revision.startswith("/"):
        raise ValueError("Invalid Git revision")
    if not 1 <= workers <= 16:
        raise ValueError("workers must be in 1..16")

    encoded_ref = urllib.parse.quote(revision, safe="")
    url = f"https://api.github.com/repos/{REPO}/git/trees/{encoded_ref}?recursive=1"
    tree = json.loads(_read(url))
    if tree.get("truncated"):
        raise RuntimeError("GitHub tree listing was truncated; cannot safely download")
    prefix = f"cases/{case_id}/"
    members = [item["path"] for item in tree.get("tree", [])
               if item.get("type") == "blob" and item["path"].startswith(prefix)]
    if not members:
        raise FileNotFoundError(f"Case not found at revision {revision}: {case_id}")

    root = Path(dest).resolve() / case_id
    root.mkdir(parents=True, exist_ok=True)
    raw_ref = urllib.parse.quote(revision, safe="/")
    base_url = f"https://raw.githubusercontent.com/{REPO}/{raw_ref}/"

    def fetch(path):
        relative = Path(path[len(prefix):])
        if any(part in ("", ".", "..") for part in relative.parts):
            raise ValueError(f"Unsafe repository path: {path}")
        payload = _read(base_url + "/".join(urllib.parse.quote(x, safe="") for x in path.split("/")))
        target = (root / relative).resolve()
        if not target.is_relative_to(root):
            raise ValueError("File escaped destination directory")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        return relative.as_posix()

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(fetch, path) for path in members]
        for future in as_completed(futures):
            future.result()

    label_file = root / "labels.csv"
    metadata_file = root / "metadata.jsonl"
    if label_file.exists() and metadata_file.exists():
        import csv
        with label_file.open(encoding="utf-8-sig", newline="") as handle:
            label_rows = list(csv.DictReader(handle))
        if label_rows and {"image", "caption"} <= set(label_rows[0]):
            labels = {row["image"]: {"caption": row["caption"]} for row in label_rows}
        elif label_rows and {"image", "label", "split"} <= set(label_rows[0]):
            labels = {
                row["image"]: {"label": row["label"], "split": row["split"]}
                for row in label_rows
            }
        else:
            raise ValueError("labels.csv has an unsupported schema")
        metadata = [json.loads(line) for line in metadata_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        if labels and "caption" in next(iter(labels.values())):
            current = {item["file_name"]: {"caption": item["text"]} for item in metadata}
        else:
            current = {
                item["file_name"]: {"label": item["label"], "split": item["split"]}
                for item in metadata
            }
        if len(labels) != len(current) or labels != current:
            raise ValueError("labels.csv and metadata.jsonl are inconsistent")
        files = {
            p.relative_to(root).as_posix()
            for p in (root / "images").rglob("*")
            if p.is_file()
        }
        if set(labels) != files:
            raise ValueError("Label entries and image files do not match")
    return root

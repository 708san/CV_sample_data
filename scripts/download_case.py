"""Download one independent case archive from GitHub Releases.

Works in Google Colab with standard Python only.
Usage:
  from scripts.download_case import download_case
  path = download_case("festival-icons", version="v1.0.0")
"""
from pathlib import Path
import hashlib
import shutil
import urllib.request
import zipfile

REPO = "708san/CV_sample_data"
CASES = {"festival-icons": {"v1.0.0": "festival-icons-v1.0.0.zip"}}

def download_case(case_id: str, version: str = "v1.0.0", dest: str = "sample_data") -> Path:
    """Download only one dataset. Raises clearly if release asset is unpublished."""
    try:
        filename = CASES[case_id][version]
    except KeyError as error:
        raise ValueError(f"Unknown case/version: {case_id}/{version}") from error
    dest_path = Path(dest).resolve()
    dest_path.mkdir(parents=True, exist_ok=True)
    archive = dest_path / filename
    url = f"https://github.com/{REPO}/releases/download/{version}/{filename}"
    try:
        urllib.request.urlretrieve(url, archive)
    except Exception as error:
        raise RuntimeError(
            f"Download failed: {url}. Check whether the Release ZIP has been published."
        ) from error
    with zipfile.ZipFile(archive) as data:
        names = data.namelist()
        prefix = f"{case_id}/"
        if not names or any(not n.startswith(prefix) for n in names):
            raise ValueError("Archive contains unexpected paths")
        for member in data.infolist():
            extracted = (dest_path / member.filename).resolve()
            if not extracted.is_relative_to(dest_path):
                raise ValueError("Unsafe path in ZIP")
        data.extractall(dest_path)
    folder = dest_path / case_id
    if not (folder / "metadata.jsonl").is_file():
        raise ValueError("Missing metadata.jsonl")
    return folder

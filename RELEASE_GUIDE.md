# Dataset releases and Colab downloads

The source of truth remains `cases/`; the two cases have independent versions.
Do **not** commit built ZIP files to the repository. Push a release tag only after
reviewing and merging verified data changes into main.

| Case | First tag | Attached assets |
| --- | --- | --- |
| Tomato leaves | `tomato-v1.2.0` | `tomato-leaves.zip`, `tomato-leaves.zip.sha256` |
| Festival icons | `festival-v1.0.0` | `festival-icons.zip`, `festival-icons.zip.sha256` |

## First release

1. Merge the GitHub Actions workflow and ZIP builder into main.
2. Enable **Settings → General → Releases → Enable release immutability**
   *before publishing*. GitHub applies this only to future releases.
3. Verify the source data, rights and labels. Note that festival-icons has
   permission for public GitHub hosting but no standard license;
   confirm release-asset redistribution is within the creators' permission.
4. Build and check locally:
   ```bash
   python scripts/build_releases.py --case tomato-leaves --tag tomato-v1.2.0
   python scripts/build_releases.py --case festival-icons --tag festival-v1.0.0
   ```
5. From an approved main commit, create and push each **new** tag:
   ```bash
   git switch main && git pull --ff-only
   git tag tomato-v1.2.0
   git tag festival-v1.0.0
   git push origin tomato-v1.2.0 festival-v1.0.0
   ```
6. A tag triggers GitHub Actions and publishes an immutable-ready Release
   with case-specific ZIP and checksum. Confirm Action success and attached assets.

## Updating

Modify a case's images, labels.csv, metadata.jsonl, and manifest.json
together; bump that case's version. After review/merge, create a **new** tag.
Never repoint tags or overwrite existing release assets.
Update Colab's explicit release tag and expected count only after release
verification. **Do not use the floating main branch or releases/latest in notebooks.**

## Integrity

The builder verifies image counts, paths, train/test split labels, metadata
and version compatibility; it creates reproducible, sorted, uncompressed ZIP
members to avoid unnecessary recompression of JPEG/PNG images.
The Notebook download cell verifies the matching .sha256 file, ZIP checksum,
paths and dataset counts, with retry and temporary extraction.

The sidecar checksum detects corruption but is not independent cryptographic
authentication. Obtain it only from the official release URL and enable
release immutability.

The existing `scripts/download_case.py` remains for older notebooks.

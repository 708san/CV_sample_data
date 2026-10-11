# Festival icons — LoRA sample case

高校文化祭の案内に使うピクトグラムの追加学習データ（ケースID: `festival-icons`）。

- v1.0.0: 180 PNG images (512×512), 60 icon concepts × 3 variants
- Captions: `metadata.jsonl` (180 JSON lines)
- Trigger token: `universal_icon_style`
- Distribution: case-specific ZIP in GitHub Releases
- Dataset archive: `festival-icons-v1.0.0.zip` (upload pending)

Release asset URL after publication:
`https://github.com/708san/CV_sample_data/releases/download/v1.0.0/festival-icons-v1.0.0.zip`

Extracted archive:
```
festival-icons/
  images/
  metadata.jsonl
  manifest.json
  labels.csv
  README.md
```

Captions follow the Hugging Face ImageFolder convention:
`{"file_name":"images/home_01.png","text":"universal_icon_style, ..."}`

**Rights:** The original 135 images are authorized for public redistribution by their creators. An explicit standardized license for downstream reuse has not yet been selected. Do not assume CC0 or CC BY.

Download instructions: see `../../scripts/download_case.py`.
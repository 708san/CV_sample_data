# CV_sample_data — 教材ケース別データ配布

この公開リポジトリでは、高校AI教材の実行用サンプルデータをケース別に管理します。

| ケースID | 内容 | 配布 |
| --- | --- | --- |
| `festival-icons` | 文化祭案内アイコンの LoRA（低ランク適応）学習用180枚 | ZIP公開待ち |
| `case-b` | 追加予定ケース | 未公開 |

## ColabからケースAだけ取得

```python
import urllib.request, zipfile
from pathlib import Path

case_id = "festival-icons"
version = "v1.0.0"
url = f"https://github.com/708san/CV_sample_data/releases/download/{version}/{case_id}-{version}.zip"
archive = Path("/content") / f"{case_id}-{version}.zip"
urllib.request.urlretrieve(url, archive)
with zipfile.ZipFile(archive) as z:
    z.extractall("/content/sample_data")
data_dir = Path("/content/sample_data") / case_id
print(data_dir / "metadata.jsonl")
```

**重要：このダウンロードURLはReleaseへのZIP登録後に有効になります。現在は未公開です。**

ケースBは別のアーカイブ名・別のフォルダを追加するだけで、ケースAのNotebookに影響しません。

初期画像135枚は制作者による一般公開の許可を得ています。正式な二次利用ライセンスはまだ設定していません。

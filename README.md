# CV_sample_data

高校生向けAI教材のコンピュータビジョン（CV）サンプルデータを、**ケースごとに独立して**公開するリポジトリです。

## ケース一覧

| ケース | 用途 | データ仕様・利用条件 |
| --- | --- | --- |
| [文化祭アイコン（festival-icons）](cases/festival-icons/) | LoRAを使った文化祭案内アイコンの生成 | [ケース別README](cases/festival-icons/README.md) |
| [トマトの葉（tomato-leaves）](cases/tomato-leaves/) | 葉の病気分類を体験する教材 | [ケース別README](cases/tomato-leaves/README.md) |

画像形式、ラベルの構造、件数、ライセンス、学習・評価上の注意事項は**各ケースのディレクトリ内**で定義します。ケース間で同じデータ形式である必要はありません。

## Google Colabでの利用

各ケースの教材Notebookから必要なケースのみ取得できます。Releaseは必要ありません。

```python
import urllib.request
exec(urllib.request.urlopen(
    "https://raw.githubusercontent.com/708san/CV_sample_data/main/scripts/download_case.py"
).read().decode("utf-8"))
data_dir = download_case("festival-icons", revision="main", dest="/content/sample_data")
print(data_dir)
```

授業でデータの再現性を保つ場合、`revision="main"` ではなく、確認済みの**コミットSHAまたはタグ**を指定してください。

取得処理の仕様は [scripts/download_case.py](scripts/download_case.py)、ケース固有の説明は各READMEを参照してください。

## データの管理

- 各ケースのデータ・仕様・ライセンス表記は、そのケース内で管理します。
- ファイル追加・削除時には、画像とラベルの整合性を検証してください。
- GitHub Releaseは任意です。正式配布時にはタグやコミットSHAによる版の固定を推奨します。

# CV_sample_data

高校生向けAI教材のコンピュータビジョン（CV）サンプルデータを、**ケースごとに独立して**公開するリポジトリです。

## ケース一覧

| ケース | 用途 | データ仕様・利用条件 |
| --- | --- | --- |
| [文化祭アイコン（festival-icons）](cases/festival-icons/) | LoRAを使った文化祭案内アイコンの生成 | [ケース別README](cases/festival-icons/README.md) |
| [トマトの葉（tomato-leaves）](cases/tomato-leaves/) | 葉の病気分類を体験する教材 | [ケース別README](cases/tomato-leaves/README.md) |

画像形式、ラベルの構造、件数、ライセンス、学習・評価上の注意事項は**各ケースのディレクトリ内**で定義します。

## Google Colabでの利用（推奨）

授業配布用のNotebookでは、画像を1枚ずつ取得するのではなく、
[GitHub Releases](https://github.com/708san/CV_sample_data/releases) の**固定タグ**から
ケース別ZIPを一度だけ取得して展開します。トマト7,209枚・文化祭168枚の各ケースは独立したReleaseを持ちます。
Releaseアセットには `.zip` と `.zip.sha256` が付き、Notebook側でハッシュを検証します。

バージョン固定、初回配布手順、更新時の運用は [RELEASE_GUIDE.md](RELEASE_GUIDE.md) を参照してください。

## 旧方式との互換性

従来の [scripts/download_case.py](scripts/download_case.py) は既存Notebookとの互換性のために残します。
これは画像を個別に取得する方式です。新しい教材では固定ReleaseのZIP方式を使ってください。

## データの管理

- 各ケースのデータ・仕様・ライセンス表記は、そのケース内で管理します。
- 画像の追加・削除時にはラベルとメタデータの整合性を検証します。
- `main` ブランチの更新だけでは、既存の固定Releaseは変化しません。

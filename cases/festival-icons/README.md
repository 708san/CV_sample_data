# 文化祭案内アイコン：LoRA学習用データ

## 教材の目的

青と白を基調とする案内アイコンの描画スタイルをLoRA（Low-Rank Adaptation）で学び、文化祭で使う**ステージアイコンを新しく生成**するサンプルケースです。

## 内容・形式

- **学習画像:** `images/` 内の 168 枚（56種類×3パターン）、512×512 PNG
- **編集用ラベル（正本）:** `labels.csv` — `image,caption` の2列。画像パスは `images/xxx.png`
- **LoRA用メタデータ:** `metadata.jsonl` — 1行1JSON、キーは `file_name` と `text`
- **仕様情報:** `manifest.json`
- **トリガーワード:** `universal_icon_style`

`metadata.jsonl` は `labels.csv` と一致させます。画像の増減・キャプション修正時は **`scripts/sync_festival_metadata.py`** で再生成・検証してください。

## 学習から除外する対象

授業で生成する**ステージアイコン**は学習データに含めません。少なくとも `music_stage` と `stage_lights` のデータは除外済みです。「ステージ」と近接する `microphone` や `music` などの一般モチーフは残してあります。完全な概念分離を意味しません。

## Colabからの取得

ルートの [README](../../README.md) のコードで `download_case("festival-icons")` を実行してください。取得先には `images/`, `labels.csv`, `metadata.jsonl`, `manifest.json` が置かれます。

## 利用条件

既存アイコンについては、制作者・制作チームからGitHubでの一般公開許可を得ています。ただし、改変・商用利用・再配布等について標準のオープンライセンスは**まだ指定されていません**。利用条件の詳細は権利者の確認が必要です。

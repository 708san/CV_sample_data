# トマトの葉の病気分類

## 教材の目的

トマトの葉の画像を、次の5クラスに分類する画像認識のサンプルです。

- `early_blight`（早期疫病）
- `healthy`（健全）
- `late_blight`（疫病）
- `septoria_leaf_spot`（セプトリア葉斑病）
- `leaf_mold`（葉かび病）

## 出典

本データの元データは、Mendeley Dataで公開されている次のデータセットです。

- Pandianj, Arun; Geetharamanigopal (2019), *Data for: Identification of Plant Leaf Diseases Using a 9-layer Deep Convolutional Neural Network*, Mendeley Data, V1
- DOI: [10.17632/tywbtsjrjv.1](https://doi.org/10.17632/tywbtsjrjv.1)
- データセットページ: [Mendeley Data](https://data.mendeley.com/datasets/tywbtsjrjv/1)
- 公開日: 2019年4月18日
- 関連論文: [10.1016/j.compeleceng.2019.04.011](https://doi.org/10.1016/j.compeleceng.2019.04.011)

元データは植物の葉・背景画像を含む39クラス、61,486枚のデータセットで、画像反転、ガンマ補正、ノイズ付加、PCAカラー拡張、回転、スケーリングの6種類の拡張手法が使われています。本リポジトリには、元データ全体ではなく、トマトに関する5クラスだけを抽出した派生データを収録しています。

## データ構成

- `images/train/<class>/` — 学習画像
- `images/test/<class>/` — テスト画像
- `labels.csv` — `image,label,split` の3列を持つ正本ラベル
- `metadata.jsonl` — 1行1JSONの機械処理用メタデータ
- `manifest.json` — 件数、クラス、分割方法、重複除去結果

クラス名は `manifest.json` の `classes` に記載しています。画像は元データの拡張子を小文字に統一し、クラス内で連番にしています。

## このケースの前処理

- 元データのトマト5クラス（early blight、healthy、late blight、leaf mold、septoria leaf spot）だけを残し、英小文字とアンダースコアによるクラス名に統一しました。
- 元データに含まれる他のトマト病害クラス（bacterial spot、target spot、tomato mosaic virus）と、トマト以外のクラスは教材の対象外として収録していません。
- SHA-256が一致する画像を重複とみなし、全クラスをまたいで重複除去してから分割しました。
- 学習5,768枚、テスト1,441枚の計7,209枚を、クラスごとにおおむね8:2で分割しました。
- 分割順はSHA-256で固定しているため、同じ入力から再現できます。
- 元データの`.DS_Store`と、画像でないファイルは含めていません。
- 画像のリサイズ、色補正などの追加変換は行っていません。

このデータは教材用の固定テストセットです。モデル選択やハイパーパラメータ調整には、学習データから別途検証用データを作成してください。

## ライセンスと出典表記

元データは [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) で公開されています。著作権法上可能な限り権利放棄されたデータであり、複製、改変、再配布、商用利用を含めて利用できます。

利用時は、次の出典表記を推奨します。

> Pandianj, Arun; Geetharamanigopal (2019), “Data for: Identification of Plant Leaf Diseases Using a 9-layer Deep Convolutional Neural Network”, Mendeley Data, Version 1, DOI: 10.17632/tywbtsjrjv.1. This repository uses a five-class tomato subset and applies deduplication and train/test splitting.

本リポジトリのデータは、元データから5クラスを抽出し、完全一致重複を除去して学習用・テスト用に分割した派生データです。

## ダウンロード

ルートの [README](../../README.md) にある `download_case("tomato-leaves")` を使って取得できます。

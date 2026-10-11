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

## ライセンスと利用条件

### 元データのライセンス表示について

確認日時点で、対象のMendeley Dataレコードには、CC BY、CC0、CC BY-NCなどの具体的なライセンス名・ライセンスURLが明示されていません。このため、本リポジトリでは元データを**自由利用可能、CC BY、CC0、または商用利用可能**とは断定しません。Mendeley Dataの利用規約だけで、個別データセットの著作権・第三者権利・再配布権が保証されるものでもありません。

利用前に、次の情報を確認してください。

1. [データセットページ](https://data.mendeley.com/datasets/tywbtsjrjv/1)に表示されるライセンス、利用条件、更新情報
2. [Mendeley Dataの利用規約](https://data.mendeley.com/terms)
3. 画像に写る人物、施設、ロゴ、または元画像の著作権など、データセットとは別に存在する第三者の権利
4. 授業、研究、公開、再配布、商用利用など、予定している利用目的に必要な許諾

### このリポジトリの位置付け

本リポジトリのデータは、元データから5クラスを抽出し、完全一致重複を除去して学習用・テスト用に分割した**派生データ**です。画像、ラベル、メタデータについて、本リポジトリが元データを超える権利や許諾を付与するものではありません。元データのライセンスが確認できない限り、再配布や公開利用の可否を独自に判断しないでください。

### 推奨する出典表記

利用が許可されていることを確認した場合は、少なくとも次を併記してください。

> Pandianj, Arun; Geetharamanigopal (2019), “Data for: Identification of Plant Leaf Diseases Using a 9-layer Deep Convolutional Neural Network”, Mendeley Data, Version 1, DOI: 10.17632/tywbtsjrjv.1. This repository uses a five-class tomato subset and applies deduplication and train/test splitting.

改変・抽出・重複除去・分割を行ったこと、および元データへのリンクとDOIを明記してください。ライセンスが後から明示された場合は、その条件と出典表記を優先し、このREADMEと`manifest.json`も更新します。

## ダウンロード

ルートの [README](../../README.md) にある `download_case("tomato-leaves")` を使って取得できます。

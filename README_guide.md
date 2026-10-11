# Colabからのデータ取得ガイド

ケースIDを指定すると、GitHubの対象ケースのファイルのみ取得できます。GitHub ReleaseやZIPの事前登録は不要です。

```python
import urllib.request

exec(urllib.request.urlopen(
    "https://raw.githubusercontent.com/708san/CV_sample_data/main/scripts/download_case.py"
).read().decode("utf-8"))

data_dir = download_case("festival-icons", revision="main", dest="/content/sample_data")
print("取得先:", data_dir)
```

`revision` にはブランチ・タグ・コミットSHAを指定できます。**授業の正式版はコミットSHAで固定**してください。

ケース固有のデータ形式や注意事項は [各ケースのREADME](cases/) に記載します。

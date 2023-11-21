# 概要


# インストール
## 依存ライブラリ
```bash
pip install -e .
```

## pre-commit
```bash
pre-commit install
```


# Usage
## Github Wikiをフェッチしてインデックスを作る
```python
from xecretary_fetcher import GithubWiki

wiki_url = <Github wikiのURL>
wiki = GithubWiki(wiki_url)
wiki.create_index()
```

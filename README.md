# easy-scraper-py

![](https://img.shields.io/static/v1?label=+&message=Python%203.9%2B&color=lightblue&logo=Python)
![](https://img.shields.io/static/v1?label=status&message=Work%20In%20Progress&color=red)
[![PyPI](https://img.shields.io/pypi/v/easy-scraper-py.svg)](https://pypi.python.org/pypi/easy-scraper-py)

An easy scraping tool for HTML

## Goal

Re-implementation of [tanakh/easy-scraper](https://github.com/tanakh/easy-scraper) in Python.

## Install from PyPI

```bash
   pip install easy-scraper-py
```

## Usage Example

```html
<!-- Target -->
<body>
    <b>NotMe</b>
    <a class=here>Here</a>
    <a class=nothere>NotHere</a>
</body>

<!-- Pattern -->
<a class=here>{{ text }}</a>
```

```python
import easy_scraper

target = r"""<body>
    <b>NotMe</b>
    <a class=here>Here</a>
    <a class=nothere>NotHere</a>
</body>
"""  # newlines and spaces are all ignored.

pattern = "<a class=here>{{ text }}</a>"

easy_scraper.match(target, pattern)  # [{'text': 'Here'}]
```

```python
# XML (RSS) scraping
import easy_scraper
import urllib.request

body = urllib.request.urlopen("https://kuragebunch.com/rss/series/10834108156628842505").read().decode()
res = easy_scraper.match(body, "<item><title>{{ title }}</title><link>{{ link }}</link></item>")
for item in res[:5]:
    print(item)
```

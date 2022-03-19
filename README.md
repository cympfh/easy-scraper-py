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

### Scraping texts

```html
<!-- Target: full or partial HTML code -->
<body>
    <b>NotMe</b>
    <a class=here>Here</a>
    <a class=nothere>NotHere</a>
</body>

<!-- Pattern: partial HTML with variables ({{ name }}) -->
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

# Matching innerText under a-tag with class="here"
pattern = "<a class=here>{{ text }}</a>"

easy_scraper.match(target, pattern)  # [{'text': 'Here'}]
```

### Scraping links

```python
target = r"""
<div>
    <div class=here>
        <a href="link1">foo</a>
        <a href="link2">bar</a>
        <a>This is not a link.</a>
        <div>
            <a href="link3">baz</a>
        </div>
    </div>
    <div class=nothere>
        <a href="link4">bazzz</a>
    </div>
</div>
"""

# Marching links (href and innerText) under div-tag with class="here"
pattern = r"""
    <div class=here>
        <a href="{{ link }}">{{ text }}</a>
    </div>
"""

assert easy_scraper.match(target, pattern) == [
    {"link": "link1", "text": "foo"},
    {"link": "link2", "text": "bar"},
    {"link": "link3", "text": "baz"},
]
```

### Scraping RSS (XML)

`easy-scraper-py` just uses [html.parser](https://docs.python.org/ja/3/library/html.parser.html) for parsing, also can parse almost XML.

```python
import easy_scraper
import urllib.request

body = urllib.request.urlopen("https://kuragebunch.com/rss/series/10834108156628842505").read().decode()
res = easy_scraper.match(body, "<item><title>{{ title }}</title><link>{{ link }}</link></item>")
for item in res[:5]:
    print(item)
```

### Scraping Images

```python
import easy_scraper
import urllib.request

url = "https://unsplash.com/s/photos/sample"
body = urllib.request.urlopen(url).read().decode()

# Matching all images
res = easy_scraper.match(body, r"<img src='{{ im }}' />")
print(res)

# Matching linked (under a-tag) images
res = easy_scraper.match(body, r"<a href='{{ link }}'><img src='{{ im }}' /></a>")
print(res)
```

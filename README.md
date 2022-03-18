# easy-scraper-py

![](https://img.shields.io/static/v1?label=+&message=Python%203.9%2B&color=lightblue&logo=Python)
![](https://img.shields.io/static/v1?label=status&message=Work%20In%20Progress&color=red)
![](https://img.shields.io/static/v1?label=pip&message=unreleased&color=red)

## Goal

Re-implementation of [tanakh/easy-scraper](https://github.com/tanakh/easy-scraper) in Python.

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

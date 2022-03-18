__all__ = ["match"]

from easy_scraper.htmlparser import HTMLParser
from easy_scraper.matching import match_html


def match(
    target: str,
    pattern: str,
) -> list[dict[str, str]]:
    """HTML Pattern Matching"""
    parser = HTMLParser()
    ref = parser(target)
    pat = parser(pattern, is_pattern=True)
    return match_html(ref, pat)

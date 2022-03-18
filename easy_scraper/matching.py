from copy import deepcopy
from typing import Optional

from easy_scraper import entity


def match_attr(x: dict, y: dict) -> Optional[dict]:
    """Matching dicts

    Returns
    -------
    Pattern matched result.
    None if failed.
    """
    ret = {}
    for k in y.keys():
        if k not in x:
            return None
        a = x[k]
        b = y[k]
        if isinstance(a, entity.PlainText) and isinstance(b, entity.PlainText):
            if a.data != b.data:
                return None
        if isinstance(a, entity.PlainText) and isinstance(b, entity.Pattern):
            ret[b.name] = a.data
    return ret


def match_siblings(ref_children: list[entity.Html], pat_children: list[entity.Html]) -> list[dict]:
    if len(ref_children) < len(pat_children):
        return []
    if len(pat_children) == 0:
        return [{}]
    ret = []
    # matching head
    head = match_html(ref_children[0], pat_children[0])
    tail = match_siblings(ref_children[1:], pat_children[1:])
    for r1 in head:
        for r2 in tail:
            ret.append(r1 | r2)
    # skip head
    ret.extend(match_siblings(ref_children[1:], pat_children))
    return ret


def match_html(ref: entity.Html, pattern: entity.Html) -> list[dict[str, str]]:
    """Matching Htmls

    Returns
    -------
    All results.
    Empty if nothing is matched.
    """
    if isinstance(ref, entity.PlainText) and isinstance(pattern, entity.PlainText):
        if ref.data == pattern.data:
            return [{}]
        else:
            return []

    elif isinstance(ref, entity.PlainText) and isinstance(pattern, entity.Pattern):
        return [{pattern.name: ref.data}]

    elif isinstance(ref, entity.Elem) and isinstance(pattern, entity.Elem):
        res = []
        # skip root of ref
        for child in ref.children:
            res.extend(match_html(child, pattern))
        # matching root
        if ref.tag == pattern.tag:
            res_attrs = match_attr(ref.attrs, pattern.attrs)
            if res_attrs is not None:
                for res_siblings in match_siblings(ref.children, pattern.children):
                    res.append(res_attrs | res_siblings)
        return res

    elif isinstance(ref, entity.Elem):
        res = []
        for child in ref.children:
            res.extend(match_html(child, pattern))
        return res

    else:
        return []

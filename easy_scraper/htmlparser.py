import html.parser
import re
from typing import Union

from easy_scraper import entity


class HTMLParser(html.parser.HTMLParser):
    def text(self, data: str) -> Union[entity.PlainText, entity.Pattern]:
        data = data.strip()
        if self.is_pattern:
            match = re.match(r"{{\s*(\w*)\s*}}", data)
            if match:
                name = match[1]
                return entity.Pattern(name)
        return entity.PlainText(data)

    def __call__(self, data: str, is_pattern: bool = False) -> entity.Elem:
        root = entity.Elem("Root", {}, [], None)
        self.cur = root
        self.is_pattern = is_pattern
        self.feed(data)
        return root

    def handle_starttag(self, tag, attrs):
        attrs = {name: self.text(data) for name, data in attrs}
        child = entity.Elem(tag, attrs, [], self.cur)
        self.cur.children.append(child)
        self.cur = child

    def handle_endtag(self, tag):
        self.cur = self.cur.parent

    def handle_data(self, data: str):
        data = data.strip()
        if not data:
            return
        child = self.text(data)
        self.cur.children.append(child)

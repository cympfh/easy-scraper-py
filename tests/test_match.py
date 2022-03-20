import pytest

import easy_scraper


class TestMatch:
    @pytest.mark.parametrize(
        "target,pattern",
        [
            ("<a>Here</a>", "<a>{{ text }}</a>"),
            ("<body><a>Here</a></body>", "<a>{{ text }}</a>"),
            ("<html><body><a>Here</a></body></html>", "<a>{{ text }}</a>"),
            (
                "<body><a class=here>Here</a><a class=nothere>NotHere</a></body>",
                "<a class=here>{{ text }}</a>",
            ),
            (
                "<body><b>NotMe</b><a class=here>Here</a><a class=nothere>NotHere</a></body>",
                "<a class=here>{{ text }}</a>",
            ),
        ],
    )
    def test_a_text(self, target, pattern):
        assert easy_scraper.match(target, pattern) == [{"text": "Here"}]

    def test_plaintext(self):
        target = r"""
        <div class=container>
            <div>
                Links:
                <a href="link1">foo</a>
                <a href="link2">bar</a>
                <div>
                    <a href="link3">baz</a>
                </div>
            </div>
        </div>
        """
        pattern = r"<div class=container>{{ text }}</div>"
        assert easy_scraper.match(target, pattern) == [
            {"text": "Links:"},
            {"text": "foo"},
            {"text": "bar"},
            {"text": "baz"},
        ]

    def test_attr(self):
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

    def test_attr_subset(self):
        target = r"""
        <div>
            <span class="x y">XY</span>
            <span class="x y z">XYZ</span>
            <span class="y z">YZ</span>
            <span class="z">Z</span>
        </div>
        """
        assert easy_scraper.match(target, "<span class='x'>{{text}}</span>") == [
            {"text": "XY"},
            {"text": "XYZ"},
        ]
        assert easy_scraper.match(target, "<span class='y z'>{{text}}</span>") == [
            {"text": "XYZ"},
            {"text": "YZ"},
        ]
        assert easy_scraper.match(target, "<span class='z'>{{text}}</span>") == [
            {"text": "XYZ"},
            {"text": "YZ"},
            {"text": "Z"},
        ]
        assert easy_scraper.match(target, "<span class='z y x'>{{text}}</span>") == [
            {"text": "XYZ"},
        ]

    def test_siblings(self):
        target = r"""
        <div>
            <ul>
                <li>1</li>
                <li>2</li>
                <li>3</li>
            </ul>
            <ul>
                <li>X</li>
                <li>Y</li>
            </ul>
        </div>
        """
        pattern = r"""
        <ul>
            <li>{{ x }}</li>
            <li>{{ y }}</li>
        </ul>
        """
        assert easy_scraper.match(target, pattern) == [
            {"x": "1", "y": "2"},
            {"x": "1", "y": "3"},
            {"x": "2", "y": "3"},
            {"x": "X", "y": "Y"},
        ]

    def test_empty(self):
        assert easy_scraper.match("<a async>OK</a>", "<a async>{{x}}</a>") == [{"x": "OK"}]
        assert easy_scraper.match("<a data=some>OK</a>", "<a data>{{x}}</a>") == [{"x": "OK"}]
        assert easy_scraper.match("<a data>NG</a>", "<a data=something>{{x}}</a>") == []

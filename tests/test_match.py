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

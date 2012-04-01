import unittest
import os
import datetime

from whitenoise.configurators import *


class TestFrontMatter(unittest.TestCase):

    def test_empty_string(self):
        content, data = parse_front_matter('')

        assert data == {}
        assert content == ''

    def test_no_yaml(self):
        content, data = parse_front_matter("""
Content
        """)

        assert data == {}
        assert content == """
Content
        """

    def test_no_content(self):
        content, data = parse_front_matter("""
---
title: Hello
---
        """)

        assert data == {
                'title': 'Hello'
                }
        assert content == ''

    def test_simple(self):
        content, data = parse_front_matter("""
---
title: Hello
---
Content
        """)

        assert data == {
                'title': 'Hello'
                }
        assert content == 'Content'

    def test_more_data(self):
        content, data = parse_front_matter("""
---
title: Hello
date: 2012-01-01
thing: [foo, bar, baz]
---
Content
        """)

        assert data == {
                'title': 'Hello',
                'date': datetime.date(2012, 1, 1),
                'thing': [
                    'foo',
                    'bar',
                    'baz',
                    ],
                }
        assert content == 'Content'

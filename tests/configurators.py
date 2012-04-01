import unittest
import os

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

import unittest
import os

from whitenoise import *
from whitenoise.configurators import parse_front_matter

base_path = os.path.join(os.path.dirname(__file__), 'build_tree')


class TestSite(unittest.TestCase):

    def test_single_file(self):
        path = os.path.join(base_path, 'single_file')
        site = Site(path)
        actual = site.build_data()

        should = {
                'url': '/single_file/',
                }
        index = {
                'filename': 'index.html',
                'url': '/single_file/',
                }

        with open(os.path.join(path, 'index.html'), 'r') as f:
            _, data = parse_front_matter(f.read())
            index.update(data)

        assert actual.data == should
        assert actual.index.data == index

    def test_flat_files(self):
        path = os.path.join(base_path, 'flat_files')
        site = Site(path)
        actual = site.build_data()

        should = {
                'url': '/flat_files/',
                }
        index = {
                'filename': 'index.html',
                'url': '/flat_files/',
                }
        foo = {
                'filename': 'foo.html',
                'url': '/flat_files/foo.html',
                }

        with open(os.path.join(path, 'index.html'), 'r') as f:
            _, data = parse_front_matter(f.read())
            index.update(data)

        assert actual.data == should
        assert actual.index.data == index
        assert actual.children[1].data == foo

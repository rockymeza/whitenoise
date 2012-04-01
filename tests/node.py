import unittest
import os

from whitenoise import *

base_path = os.path.join(os.path.dirname(__file__), 'node')


class TestNode(unittest.TestCase):

    def test_index(self):
        path = os.path.join(base_path, 'index.html')
        node = Node(path)

        assert node.is_index()

        path = os.path.join(base_path, 'index.md')
        node = Node(path)

        assert node.is_index()

        path = os.path.join(base_path, 'index.html.jinja')
        node = Node(path)

        assert node.is_index()

import unittest
import os

from whitenoise.tree import *

base_path = os.path.join(os.path.dirname(__file__), 'build_tree')


class TestBuildTree(unittest.TestCase):

    def test_single_file(self):
        path = os.path.join(base_path, 'single_file')

        should = Directory(path)
        should.index = Node(os.path.join(path, 'index.html'))

        actual = build_tree(path)

        assert should == actual

    def test_flat_files(self):
        path = os.path.join(base_path, 'flat_files')

        should = Directory(path)
        should.index = Node(os.path.join(path, 'index.html'))

        bar = Node(os.path.join(path, 'bar.html'))
        foo = Node(os.path.join(path, 'foo.html'))
        should.children.append(bar)
        should.children.append(foo)

        actual = build_tree(path)

        assert should == actual

    def test_hiearchical(self):
        path = os.path.join(base_path, 'hierarchical')

        should = Directory(path)
        should.index = Node(os.path.join(path, 'index.html'))

        secondary = Directory(os.path.join(path, 'secondary'))
        bar = Node(os.path.join(secondary.path, 'bar.html'))
        secondary.children.append(bar)
        should.children.append(secondary)

        foo = Node(os.path.join(path, 'foo.html'))
        should.children.append(foo)

        actual = build_tree(path)

        assert should == actual

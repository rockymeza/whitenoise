import os


def build_tree(path, configurate_dir=None, configurate_file=None, parent=None):
    """
    `build_tree` takes the path of a directory and returns a tree based
    on the filesystem.  This method takes two optional callbacks for data
    pre-processing.
    """

    base = Directory(path)

    if parent:
        base.parent = parent

    if configurate_dir:
        configurate_dir(base)

    for f in os.listdir(base.path):
        if f.startswith('.'): continue

        current_path = os.path.join(base.path, f)

        if os.path.isdir(current_path):
            sub = build_tree(current_path, configurate_dir, configurate_file, base)

            base.children.append(sub)
        else:
            node = Node(current_path)
            node.parent = base
            
            if configurate_file:
                configurate_file(node)

            if node.is_index():
                base.index = node
            else:
                base.children.append(node)

    return base


class Directory(object):
    """
    A Directory is a directory.  It has children which can be either
    Nodes or more Directories.  It also has a special index attribute
    which corresponds to the index file for that directory.
    """
    def __init__(self, path):
        self.path = path
        _, self.name = os.path.split(path)
        self.index = None
        self.data = {}
        self.parent = None
        self.children = []

    def __eq__(self, b):
        return b and \
               self.path == b.path and \
               self.index == b.index and \
               self.data == b.data and \
               self.children == b.children


class Node(object):
    """
    A Node is a file.  Any YAML front matter that it has will be
    populated into the data attribute.
    """
    def __init__(self, path):
        self.path = path
        self.data = {}
        _, self.data['filename'] = os.path.split(path)
        self.parent = None

    def __eq__(self, b):
        return b and \
               self.path == b.path and \
               self.data == b.data

    def is_index(self):
        """
        Files whose name start with "index." are treated specially.  When
        looping through a directory, they will not appear.
        """
        return self.data['filename'].startswith('index.')

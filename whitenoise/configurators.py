"""
Configurators are functions that are used to customize the data building process.
"""
import os
import re
import yaml

from whitenoise.tree import Directory, Node


class Configurator(object):
    def __call__(self, thing):
        try:
            if isinstance(thing, Directory):
                self.configurate_dir(thing)
            elif isinstance(thing, Node):
                self.configurate_file(thing)
        except NotImplementedError:
            pass

    def configurate_dir(self, directory):
        raise NotImplemented

    def configurate_file(self, node):
        raise NotImplemented


front_matter_re = re.compile('^---\\s*\\n([\\s\\S]*?\\n?)^---\\s*$\\n?', re.M)


def parse_front_matter(content):
    """
    Returns a tuple of content and extracted data.
    """
    match = front_matter_re.search(content)

    if match:
        content = content[match.end(0):].strip()
        data = yaml.load(match.group(1))
    else:
        data = {}

    return (content, data)


def front_matter_configurator(node):
    with open(node.path, 'r') as f:
        node.content, data = parse_front_matter(f.read())
        node.data.update(data)


class URLConfigurator(Configurator):
    def __init__(self, pattern, root_url=None):
        self.pattern = pattern
        self.root_url = root_url or '/'

    def configurate_dir(self, directory):
        path = directory.name
        if directory.parent:
            path = directory.parent.data['url'] + path
            directory.data['url'] = path + '/'
            target = os.path.join(directory.parent.data['target'], path)
            directory.data['target'] = directory.data['url']
        else:
            directory.data['url'] = self.root_url
            directory.data['target'] = ''

    def configurate_file(self, node):
        sub_part = self.pattern.format(**node.data)

        if node.is_index():
            node.data['url'] = node.parent.data['url']
        else:
            node.data['url'] = node.parent.data['url'] + sub_part

        node.data['target'] = os.path.join(node.parent.data['target'], sub_part)

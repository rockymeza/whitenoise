import os

from whitenoise.tree import *
from whitenoise.configurators import *
import whitenoise.jinja as jinja


url_configurator = URLConfigurator('{filename}')
jinja_support = jinja.JinjaSupport(
        'layouts',
        extensions=jinja.DEFAULT_EXTENSIONS,
        filters=jinja.DEFAULT_FILTERS,
        )

DEFAULT_DIR_CONFIGURATORS = [
        url_configurator,
        ]
DEFAULT_FILE_CONFIGURATORS = [
        front_matter_configurator,
        url_configurator,
        jinja_support.file_configurator,
        ]

DEFAULT_FILE_PROCESSORS = [
        jinja_support.processor,
        ]


class Site(object):
    
    def __init__(self, root, dir_configurators=None, file_configurators=None, file_processors=DEFAULT_FILE_PROCESSORS):
        self.root = root
        self.dir_configurators = dir_configurators or DEFAULT_DIR_CONFIGURATORS
        self.file_configurators = file_configurators or DEFAULT_FILE_CONFIGURATORS
        self.file_processors = file_processors or DEFAULT_FILE_PROCESSORS

    def build_data(self):
        data = build_tree(self.root, self.configurate_dir, self.configurate_file)

        return data

    def configurate_dir(self, directory):
        for configurator in self.dir_configurators:
            configurator(directory)

    def configurate_file(self, node):
        for configurator in self.file_configurators:
            configurator(node)

    def process_file(self, node):
        for processor in self.file_processors:
            processor(node)

    def generate(self, destination):
        root = self.build_data()
        
        try:
            os.mkdir(destination)
        except OSError:
            pass

        generate_directory(root, destination, self.process_file)


def generate_directory(directory, destination, process_file=None):
    target = os.path.join(destination, directory.data['target'])
    try:
        os.mkdir(target)
    except OSError:
        pass

    if directory.index:
        copy_file(directory.index, destination, process_file)

    for child in directory.children:
        if isinstance(child, Directory):
            generate_directory(child)
        else:
            copy_file(child, destination, process_file)


def copy_file(node, destination, process_file=None):
    target = os.path.join(destination, node.data['target'])
    if process_file:
        process_file(node)
    with open(target, 'w') as f:
        f.write(node.content)

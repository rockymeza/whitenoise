import os

from whitenoise.tree import *
from whitenoise.configurators import *


url_configurator = URLConfigurator('{filename}')
DEFAULT_DIR_CONFIGURATORS = [
        url_configurator,
        ]
DEFAULT_FILE_CONFIGURATORS = [
        front_matter_configurator,
        url_configurator,
        ]


class Site(object):
    
    def __init__(self, root, dir_configurators=None, file_configurators=None):
        self.root = root
        self.dir_configurators = dir_configurators or DEFAULT_DIR_CONFIGURATORS
        self.file_configurators = file_configurators or DEFAULT_FILE_CONFIGURATORS

    def build_data(self):
        data = build_tree(self.root, self.configurate_dir, self.configurate_file)

        return data

    def configurate_dir(self, directory):
        for configurator in self.dir_configurators:
            configurator(directory)

    def configurate_file(self, node):
        for configurator in self.file_configurators:
            configurator(node)

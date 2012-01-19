from strange_case_jinja import StrangeCaseEnvironment
from extensions.markdown2_extension import Markdown2Extension, markdown2
from extensions.date_extension import date
from node import FolderNode, JinjaNode
from time import time
from datetime import datetime
import os

ENVIRONMENT = StrangeCaseEnvironment(extensions=[Markdown2Extension])
ENVIRONMENT.filters['date'] = date
ENVIRONMENT.filters['markdown2'] = markdown2


CONFIG = {
    'time': int(time()),
    'now': datetime.today(),
}


from processor import Registry, Processor


class CategoriesProcessor(Processor):
    name = 'categories'
    look_in = ''  # can be a dot-separated path (or paths).  Do not include 'site' in this path (e.g. 'blogs' not 'site.blogs')
    insert_at = ''  # adds the category index at this dot-separated node.  Do not include 'site' in this path (e.g. 'blogs' not 'site.blogs')

    def get_node_at(self, site, path):
        paths = filter(bool, path.split('.'))
        look_in_node = site
        while len(paths):
            look_in_node = getattr(look_in_node, paths.pop(0))
        return look_in_node

    def populate(self, site):
        if isinstance(self.look_in, basestring):
            look_ins = [self.look_in]
        else:
            look_ins = self.look_in

        look_in_nodes = []
        for look_in_path in look_ins:
            look_in_nodes.append(self.get_node_at(site, look_in_path))

        insert_at_node = self.get_node_at(site, self.insert_at)

        categories = {}
        for look_in_node in look_in_nodes:
            for page in look_in_node.all(everything=True):
                if page.category:
                    count = categories.get(page.category, 0)
                    categories[page.category] = count + 1

        category_config = site.config_copy(self.name, self.name)
        category_target = os.path.join(site.folder, self.name)
        category_index = Register.get('page', category_config, None, category_target)
        insert_at_node.append(category_index)

        category_config = site.config_copy(category_config['index'], self.name)
        category_target = site.folder(category_index.folder, category_config['index'])
        category_root = Register.get('folder', category_config, None, category_target)
        insert_at_node.append(category_root)

        for category in categories:
            insert_at_node.append()

    def process(self, config, source_path, target_path, public_path):
        return (FolderNode(config, public_path, None, target_path),)

# Registry.register('category_page', CategoriesProcessor)


class CategoriesNode(FolderNode):
    """
    Renders a category index page and a category browse page for each
    category in the site.  Can be filtered to a specific directory by
    specifying "root" as a dot-delimited path to a folder.
    """
    def generate(self, site):
        # template = JinjaNode.get_environment().get_template(self.source)
        # content = template.render(self.config, my=self, **context)

        # target = os.path.join(self.target, self.target_name)
        # with open(target, 'w') as dest:
        #     dest.write(content.encode('utf-8'))
        print site


class CategoryNode(JinjaNode):
    pass

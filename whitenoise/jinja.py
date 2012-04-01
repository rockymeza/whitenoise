import datetime

from jinja2 import Environment, DictLoader, PrefixLoader, FileSystemLoader

class JinjaSupport(object):
    def __init__(self, layouts_dir, filters=None, extensions=None):
        self.should_process = []
        self.loader = DictLoader({})
        self.env = Environment(
                loader=PrefixLoader({
                    'layouts': FileSystemLoader(layouts_dir),
                    'nodes': self.loader,
                    }, '::'),
                extensions=extensions or [],
                )

        self.env.filters.update(filters)

    def file_configurator(self, node):
        if node.data['filename'].endswith('.jinja'):
            node.data['target'] = node.data['target'].rstrip('.jinja')
            node.data['url'] = node.data['url'].rstrip('.jinja')
            self.loader.mapping[node.data['target']] = node.content

            self.should_process.append(node)

    def processor(self, node):
        if node in self.should_process:
            template = self.env.get_template('nodes::' + node.data['target'])
            node.content = template.render(page=node.data)



def date(value, format='%Y %b %d'):
    if not value:
        return ''

    if value is "now":
        value = datetime.date.today()
    elif isinstance(value, basestring):
        value = datetime.datetime.strptime(value, "%Y-%m-%d")
    elif isinstance(value, int) or isinstance(value, float):
        value = datetime.date.fromtimestamp(value)

    if isinstance(value, datetime.date):
        return value.strftime(format)


DEFAULT_EXTENSIONS = [
        ]
DEFAULT_FILTERS = {
        'date': date,
        }

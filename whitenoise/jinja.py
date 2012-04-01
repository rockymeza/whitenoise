import datetime

import jinja2
import jinja2.ext
from misaka import Markdown, HtmlRenderer, EXT_FENCED_CODE, EXT_NO_INTRA_EMPHASIS, HTML_SMARTYPANTS

class JinjaSupport(object):
    def __init__(self, layouts_dir, filters=None, extensions=None):
        self.should_process = []
        self.loader = jinja2.DictLoader({})
        self.env = jinja2.Environment(
                loader=jinja2.PrefixLoader({
                    'layouts': jinja2.FileSystemLoader(layouts_dir),
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

    def processor(self, site_data, node):
        if node in self.should_process:
            template = self.env.get_template('nodes::' + node.data['target'])
            node.content = template.render(site=site_data, page=node.data)



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
 


renderer = HtmlRenderer(HTML_SMARTYPANTS)
markdowner = Markdown(renderer, EXT_FENCED_CODE | EXT_NO_INTRA_EMPHASIS)


def markdown(text):
    return markdowner.render(text).strip()


class Markdown2Extension(jinja2.ext.Extension):
    tags = set(['markdown'])

    def __init__(self, environment):
        super(Markdown2Extension, self).__init__(environment)
        environment.extend(
            markdowner=markdowner
        )

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        body = parser.parse_statements(
            ['name:endmarkdown'],
            drop_needle=True
        )
        return jinja2.nodes.CallBlock(
            self.call_method('_markdown_support'),
            [],
            [],
            body
        ).set_lineno(lineno)

    def _markdown_support(self, caller):
        return self.environment.markdowner.render(caller()).strip()


DEFAULT_EXTENSIONS = [
        Markdown2Extension,
        ]
DEFAULT_FILTERS = {
        'date': date,
        'markdown': markdown,
        }

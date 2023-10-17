# -*- coding: utf-8 -*-
"""Creates a table of functions.
"""

import inspect
import textwrap
from ..utils import tableasmd
from .utils import apiobj

__all__ = [
    'funcstable'
]


@apiobj
def funcstable(funcs, hostdoc=None, indent=None) -> str:
    """Returns functions overview as an MD table.

    Parameters
    ----------
    funcs : list
        Functions to be inspected.
    hostdoc : str = None
        Name of the parent MD document.
        If given, links to functions are generated.
    indent : int = None
        Specifies the table indent, if needed.

    """

    maker = FuncsTable()
    maker.setconfig(indent, hostdoc)

    return maker.maketable(funcs)


class FuncsTable:
    """Creates a table of functions.
    """

    def __init__(self):
        self._indent = 0
        self._hostname = None

    def setconfig(self, indent, hostname):
        self._indent = indent
        self._hostname = hostname

    def maketable(self, funcs):
        columns = self.getcolumns(funcs)
        return self.build_table(columns)

    def getcolumns(self, funcs):
        return getattr(self, 'getcolumns_')(funcs)

    def build_table(self, columns):
        table = self.run_maketable(columns)
        text = self.indent_text(table, self._indent)
        return text

    def run_maketable(self, columns):
        return tableasmd.maketablemd(columns)

    def getcolumns_(self, funcs):

        links = self.get_linked_names(funcs)
        signs = self.get_signatures(funcs)
        infos = self.get_descriptions(funcs)

        links.insert(0, 'Name')
        signs.insert(0, 'Call')
        infos.insert(0, 'Description')

        return [
            links, signs, infos
        ]

    def get_linked_names(self, methods) -> list[str]:
        names = self.fetch_names(methods)
        links = self.make_links(names)
        return links

    def get_signatures(self, funcs) -> list[str]:
        return list(
            map(SignDumper().dumpsign, funcs)
        )

    def get_descriptions(self, funcs) -> list[str]:
        docs = self.getdocs(funcs)
        annotations = self.getannots(docs)
        return annotations

    def make_links(self, names):
        return list(
            map(self.name_to_link, names)
        )

    def name_to_link(self, name):
        if self._hostname is None:
            return self.link_no_hostname(name)
        return self.link_with_hostname(name)

    def link_no_hostname(self, name):
        return f'<b>{name}</b>'

    def link_with_hostname(self, name):
        path = self._hostname + '#' + name
        return f'<a href="{path}">{name}</a>'

    def getdocs(self, funcs):

        def _getdoc(func):
            return func.__doc__ or ''

        return list(
            map(_getdoc, funcs)
        )

    def getannots(self, docs):
        return list(
            map(self.fetch_annotation, docs)
        )

    def fetch_names(self, objs):
        return [
            obj.__name__ for obj in objs
        ]

    def fetch_annotation(self, doc):
        firstline, _, _ = doc.partition('\n')
        return firstline.strip()

    def indent_text(self, text, indent):
        if not indent:
            return text
        return textwrap.indent(
            text, prefix=chr(32)*indent
        )


class SignDumper:
    """Dumps signatures of python callables.
    """

    def dumpsign(self, obj):
        sign = self.getsign(obj)
        sign = self.editsign(sign)
        sign = self.rendersign(sign)
        return sign

    def getsign(self, obj):
        return Signature().fromobj(obj)

    def editsign(self, sign):
        return self.filter_params(sign)

    def filter_params(self, sign):
        return sign.filter_params()

    def rendersign(self, sign):
        sign = sign.render()
        return f'<i>{sign}</i>'


class Signature:
    """Signature of a python callable.
    """

    def __init__(self):
        self._params = None
        self._returns = None

    def fromobj(self, obj):
        sign = self.sign_as_str(obj)
        return self.parse_sign(sign)

    def parse_sign(self, sign):
        self._params = self.fetch_params(sign)
        self._returns = self.fetch_returns(sign)
        return self

    def fetch_returns(self, sign):
        _, _, returns = sign.partition('->')
        return returns.strip()

    def fetch_params(self, sign) -> list[str]:

        body, *_ = sign.partition('->')
        body = body.strip('( )')

        return [
            param.strip() for param in body.split(',')
        ]

    def sign_as_str(self, obj):
        return str(
            inspect.signature(obj)
        )

    def render(self) -> str:
        body = self.render_body()
        returns = self.render_returns()
        return self.assemble(body, returns)

    def render_body(self):
        params = ', '.join(self._params)
        return f'({params})'

    def render_returns(self):
        if not self._returns:
            return ''
        return ' → ' + self._returns

    def filter_params(self) -> None:
        self.removeself()
        self.removecls()
        return self

    def removeself(self):

        params = self._params

        if 'self' in params:
            params.remove('self')

    def removecls(self):

        params = self._params

        if 'cls' in params:
            params.remove('cls')

    def assemble(self, *parts):
        return ''.join(
            filter(len, parts)
        )

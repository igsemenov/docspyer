# -*- coding: utf-8 -*-
"""Generates deep non-extendable trees from a name-to-names mapping.
"""


def maketrees(name_to_names) -> list:
    """Makes deep non-extendable trees from a name-to-names mapping.

    Parameters
    ----------
    name_to_names : dict
        Name-to-name mapping to process.

    Returns
    -------
    list[TreeNode]
        Roots of the resulting trees.

    """
    trees_maker = TreesMaker()
    roots = trees_maker.make_trees(name_to_names)
    return roots


class TreesMaker:
    """Makes deep non-extendable trees from a name-to-names mapping.
    """

    def make_trees(self, name_to_names: dict) -> list:

        roots: list = self.create_two_level_trees(name_to_names)

        roots = self.expand_two_level_trees(roots)
        roots = self.remove_empty_roots(roots)

        return roots

    def expand_two_level_trees(self, roots: list) -> list:

        rootnames = [
            root.name for root in roots
        ]

        for rootname in rootnames:
            roots = self.handle_a_tree(rootname, roots)

        return roots

    def handle_a_tree(self, rootname, roots) -> list:
        touched = self.run_tree_expander(roots, rootname)
        roots = self.remove_touched_roots(roots, touched)
        return roots

    def run_tree_expander(self, roots, rootname):

        root_fetcher = self.fetch_root_by_name
        root = root_fetcher(roots, rootname)

        if root is None:
            return roots

        touched_roots = expand_tree(root=root, subroots=roots)
        return touched_roots

    def fetch_root_by_name(self, roots, name):
        for root in roots:
            if root.name == name:
                return root
        return None

    def remove_touched_roots(self, roots, touched_roots) -> list:
        def is_not_touched(root):
            return root.name not in touched_roots
        return list(
            filter(is_not_touched, roots)
        )

    def remove_empty_roots(self, roots) -> list:
        def is_non_empty(root):
            return bool(root.children) is True
        return list(
            filter(is_non_empty, roots)
        )

    def create_two_level_trees(self, name_to_names: dict) -> list:

        items = name_to_names.items()
        treemaker = self.make_two_level_tree

        primary_roots = [
            treemaker(name, names) for name, names in items
        ]

        return primary_roots

    def make_two_level_tree(self, name, names):

        root = TreeNode(name)

        root.children = list(
            map(TreeNode, names)
        )

        return root


def expand_tree(root, subroots) -> list[str]:
    """Replaces terminal nodes with subtrees where possible.

    Parameters
    ----------
    root : TreeNode
        Root of the source tree.
    subroots : Iterable[TreeNode]
        Roots of the candidate subtrees.

    Returns
    -------
    list[str]
        Names of the inserted subroots.

    """

    if not subroots:
        return []

    tree_expander = TreeExpander(root, subroots)
    return tree_expander.expand_tree()


class TreeExpander:
    """Extends a single tree by inserting subtrees.
    """

    def __init__(self, root, subroots):

        self.set_root_node(root)
        self.set_tree_copier()
        self.set_subroots_namespace(subroots)
        self.touched_subroots: list[str] = []

    def set_root_node(self, root):
        self.root = root

    def set_tree_copier(self):
        self.tree_copier = TreeCopier()

    def set_subroots_namespace(self, subroots):
        self.subroots_namespace = {
            root.name: root for root in subroots
        }

    def expand_tree(self) -> list:

        repeat = True
        touched_subroots = []

        while repeat is True:

            self.walk_and_expand()
            repeat = self.repeat_if_touched()

            touched_subroots.extend(self.touched_subroots)

        return touched_subroots

    def walk_and_expand(self) -> list:

        operators = [
            self._reset_state,
            self._invoke_walker,
            self._remove_touched_subroots
        ]

        for operator in operators:
            operator()

    def _reset_state(self):
        list.clear(self.touched_subroots)

    def _invoke_walker(self):
        getattr(self, 'walk_to_expand')(self.root)

    def _remove_touched_subroots(self):
        for subrootname in self.touched_subroots:
            if subrootname in self.subroots_namespace:
                dict.pop(self.subroots_namespace, subrootname)

    def repeat_if_touched(self) -> bool:
        if self.touched_subroots:
            return True
        return False

    def walk_to_expand(self, node):

        if node.children is None:

            status = self.is_node_to_expand(node)
            self.add_subtree_if_true(node, status)

            return

        for child in node.children:
            self.walk_to_expand(child)

    def add_subtree_if_true(self, node, status):

        if not status:
            return

        subroot = self.subroots_namespace[node.name]

        copytree = self.tree_copier.walk_to_copy_tree
        copytree(subroot, node)

        list.append(
            self.touched_subroots, node.name
        )

    def is_node_to_expand(self, node) -> bool:

        is_root = self.is_root_node
        is_touched = self.is_touched_subroot
        is_subtree = self.is_in_subroots_namespace

        if is_root(node) or is_touched(node):
            return False
        if is_subtree(node):
            return True

        return False

    def is_root_node(self, node):
        return node.name == self.root.name

    def is_touched_subroot(self, node):
        return node.name in self.touched_subroots

    def is_in_subroots_namespace(self, node):
        return node.name in self.subroots_namespace


class TreeCopier:
    """Copy a tree starting from the root.
    """

    def walk_to_copy_tree(self, node, twin):

        if not node.children:
            return

        twin = self.copy_children(node, twin)

        children = zip(node.children, twin.children)

        for node_, twin_ in children:
            self.walk_to_copy_tree(node_, twin_)

    def copy_children(self, node, twin):

        twin.children = [
            TreeNode(child.name) for child in node.children
        ]

        return twin


class TreeNode:
    """Node of the resulting trees.

    Attributes
    ----------
    name : str
        Node name as a label.
    data : str
        Node name as data for the tree printer.
    children : list[TreeNode] | None
        Children nodes.

    """

    def __init__(self, name):
        self.name = name
        self.data = name
        self.children = None

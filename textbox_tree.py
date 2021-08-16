"""
Rather that having to deal with the complicated logic of implementing response textboxes
following a choice from a Choice Textbox, the TextBox Tree allow for easy collection and
management of textboxes.
"""
import text_box

class Textbox_Tree_Node:

    def __init__(self):
        """
        Initalizes a node that is a part of a textbox tree. Like all
        binary trees nodes, each node is assumed to be the parent
        (i.e. you can only go downward from the tree, not up).

        In addition, there will be no Textbox Tree class; a Textbox Tree
        will be represented by a bunch of nodes connected to each other.

        """
        raise NotImplementedError

"""
Rather that having to deal with the complicated logic of implementing response textboxes
following a choice from a Choice Textbox, the TextBox Tree allow for easy collection and
management of textboxes.
"""
import text_box

class Textbox_Tree_Node:

    def __init__(self, textbox_object, yes_child = None, no_child = None):
        """
        Creates a new Textbox Tree Node.

        Parameters:
            - the actual textbox object that the node points to
            - the textbox response for the YES and NO responses,
              if textbox object is a choice textbox
        """
        self.textbox_object = textbox_object
        self.yes_child = yes_child
        self.no_child = no_child
        return

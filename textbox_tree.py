"""
Rather that having to deal with the complicated logic of implementing response textboxes
following a choice from a Choice Textbox, the TextBox Tree allow for easy collection and
management of textboxes.

USEFUL RESOURCES:
    - https://docs.python.org/3/library/exceptions.html
    - https://docs.python.org/3/tutorial/errors.html
"""
import text_box

class Textbox_Tree_Node:

    def __init__(self, textbox_object, yes_child = None, no_child = None, next_child = None):
        """
        Creates a new Textbox Tree Node.

        Parameters:
            - the actual textbox object that the node points to
            - the textbox response for the YES and NO responses,
              if textbox object is a choice textbox
            - the next textbox object to render, if textbox node represents a non-choice
              textbox
        """
        self.textbox_object = textbox_object
        self.yes_child = yes_child
        self.no_child = no_child
        self.next_child = next_child
        self.frames_since_shown = 0
        return

    def is_choice_textbox(self):
        """
        Returns True if the textbox is a Choice Textbox, and False
        otherwise.
        """
        if isinstance(self.textbox_object, Choice_Textbox()):
            return True
        else:
            return False

    def increment_frames(self):
        self.frames_since_shown += 1
        return

    def reset_frames(self):
        self.frames_since_shown = 0
        return


class Textbox_Tree:

    def __init__(self, head):
        """
        Creates a new Textbox Tree.

        Parameters:
            The Textbox Tree Node that will be the head of the tree.
        """
        self.head = head

        # The current textbox that we need to render
        self.current = self.head

        return

    def make_choice(self, choice):
        """
        Renders the needed textbox depending on the choice the user
        makes on the current textbox (assuming that the textbox is a
        Choice Textbox).

        Parameters:
            the YES/NO choice represented as a boolean value
                True == YES
                False == NO

        Returns:
            No return value, but the function sets self.current
            to the textbox corresponding to the YES/NO value.
        """
        if !self.head.is_choice_textbox():
            raise TypeError

        self.frames_since_shown = 0
        if choice == True:
            self.current = self.current.yes_child
        else:
            self.current = self.current.no_child

        return

    def next_textbox(self):
        """
        Renders the next textbox if current textbox is not a Choice Textbox.
        """
        if self.head.is_choice_textbox():
            raise TypeError

        self.frames_since_shown = 0
        self.current = self.current.next_child
        return

    def reset_tree(self):
        """
        Resets the current textbox to the head textbox, so the textbox
        interactions play out the same the next time these set of textboxes are rendered.
        """
        self.current = self.head
        return

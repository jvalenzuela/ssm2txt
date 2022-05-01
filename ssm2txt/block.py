"""
This module defines classes to generate documentation at the block level of
the project tree.
"""


from ssm2txt.base import Node
from ssm2txt.doc import Documentation
import ssm2txt.mttfd as mttfd


class MTTFD(mttfd.MTTFD):
    """The MTTFD tab."""

    child_type = 'elements'

    @property
    def show(self):
        """
        Filter condition to exclude this tab if the parent subsystem MTTFD
        is not determined from blocks.
        """
        channel = self.parent.parent
        subsystem = channel.parent
        return not subsystem.mttfd_direct


class Block(Node):
    """Generates output for blocks."""

    acronym = 'BL'
    parent_attr = 'parentopoid'
    tabs = [Documentation, MTTFD]

    @property
    def show_children(self):
       """
       Filter condition to exclude elements if MTTFD is entered directly
       and DC is not determined from elements.
       """
       return (not self.mttfd_direct
               or self.element.attrib['dcdet'] == 'detSubItems')

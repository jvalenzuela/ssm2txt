"""
This module defines classes to generate documentation at the block level of
the project tree.
"""


from ssm2txt.base import Node
from ssm2txt.dc import DC
from ssm2txt.doc import Documentation
import ssm2txt.mttfd as mttfd


class MTTFD(mttfd.MTTFD):
    """The MTTFD tab."""

    child_type = 'elements'


class Block(Node):
    """Generates output for blocks."""

    acronym = 'BL'
    parent_attr = 'parentopoid'
    tabs = [Documentation, MTTFD, DC]

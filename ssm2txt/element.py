"""
The module defines classes to generate documentation at the element level
of the project tree.
"""


from ssm2txt.base import Node
from ssm2txt.doc import Documentation
import ssm2txt.mttfd as mttfd


class MTTFD(mttfd.MTTFD):
    """The MTTFD tab."""

    child_type = None


class Element(Node):
    """Generates output for elements."""

    acronym = 'EL'
    parent_attr = 'parentopoid'
    tabs = [Documentation, MTTFD]

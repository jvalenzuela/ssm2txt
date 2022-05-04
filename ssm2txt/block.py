"""
Copyright 2022 Jason Valenzuela

This file is part of ssm2txt.

ssm2txt is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

ssm2txt is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
ssm2txt. If not, see <https://www.gnu.org/licenses/>.

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

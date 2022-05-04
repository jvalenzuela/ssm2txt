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

This module defines the object handling content for channel nodes in the
project tree.
"""


from ssm2txt.base import Node


class Channel(Node):
    """Generates output for a channel node.

    Channels do not have any content(tabs), but serve only as an organizational
    unit.
    """

    parent_attr = 'componentopoid'
    tabs = []

    # Mapping of channel type to display name.
    names = {
        'ch1': 'Channel 1',
        'ch2': 'Channel 2',
        'chTest': 'Test Channel'
    }

    @property
    def name(self):
        """Channel names are fixed based on the channel type."""
        return self.names[self.ch_type]

    @property
    def acronym(self):
        """Channels use different acronyms between the 1/2 and test channels."""
        return 'TE' if 'Test' in self.ch_type else 'CH'

    @property
    def ch_type(self):
        """The channel type raw attribute value."""
        return self.element.attrib['channeltype']

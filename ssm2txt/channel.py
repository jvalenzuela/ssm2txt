"""
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

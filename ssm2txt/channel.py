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

    # Identifies which channels are present in each of the categories.
    categories = {
        'Unknown': (),
        'B': ('ch1',),
        '1': ('ch1',),
        '2': ('ch1', 'chTest'),
        '3': ('ch1', 'ch2'),
        '4': ('ch1', 'ch2')
    }

    # Mapping of channel type to display name.
    names = {
        'ch1': 'Channel 1',
        'ch2': 'Channel 2',
        'chTest': 'Test Channel'
    }

    @property
    def show(self):
        """
        All channel types are always present in the source XML, so this
        filters out those not relevant based on subsystem configuration.
        """
        # Exclude channels not part of the subsystem's category.
        include = self.ch_type in self.categories[self.parent.category]

        # Test channels are always excluded if the parent subsystem
        # uses MTTFD direct entry.
        if (self.ch_type == 'chTest') and self.parent.mttfd_direct:
            include = False

        return include

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

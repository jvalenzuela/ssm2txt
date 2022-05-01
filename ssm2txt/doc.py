"""
This module defines a common Documentation tab used for subsystems, blocks,
and elements.
"""


from ssm2txt.base import Tab


class Documentation(Tab):

    fields = [
        (None, 'name'),
        ('Reference designator', 'equipmentid'),
        ('Inventory number', 'inventoryno'),
        ('Device Manufacturer', 'manufacturer'),
        ('Device Identifier', 'deviceid'),
        ('Device group', 'devicegroup'),
        ('Part number', 'partno'),
        ('Revision', 'revision'),
        ('Function', 'functiontypes'),
        ('Technology', 'technology'),
        ('Category', 'cat', 'show_cat'),
        ('Use case', 'usecase'),
        ('Description of the use case', 'usecasedocumentation'),
        ('Documentation', 'description'),
        ('Document', 'document')
    ]

    @property
    def show_cat(self):
        """
        Excludes the Category field in subsystems, which have a dedicated
        Category tab.
        """
        return not 'catconditions' in self.element.attrib

    def format_name(self, raw):
        """Formats the name field based on the type of parent node."""
        return "Name of {0}: {1}".format(type(self.parent).__name__.lower(),
                                         raw)

    def format_functiontypes(self, raw):
        """Formats the set of function checkboxes."""
        funcs = [f[3:] for f in raw.split(',')] # Strip the 'fnc' prefix.
        funcs.sort() # Display order is also alphabetic.
        return ', '.join(funcs)

    def format_technology(self, raw):
        """Formatter for the technology field."""
        return raw[3:].lower()

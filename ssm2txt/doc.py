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
        """Filter condition to exclude the category field."""
        return True

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

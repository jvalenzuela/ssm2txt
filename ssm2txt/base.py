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

This module defines a set of base classes which organize content into
sections. Their implementation closely follows that employed by the
SISTEMA GUI, specifically the project tree and tabs, such that the
generated output can be easily correlated with the source project.
"""


import collections


class Base(object):
    """Base class for all sectioning types."""

    def __init__(self, element, nodes, doc):
        self.element = element
        self.nodes = nodes
        self.doc = doc

    @property
    def oid(self):
        """The OID string assigned to this element."""
        return self.element.attrib['oid']

    @property
    def node(self):
        """The directly-associated node object.

        This will be self for Node instances, or the parent node for Tabs.
        """
        return self.nodes[self.oid]


class Node(Base):
    """
    Base class for a node on the SISTEMA project tree, such as a safety
    function or subsystem. It serves as a container for tabs and child
    nodes.
    """

    # Characters used to draw the title block and project tree.
    BORDER_LEFT = chr(9553)
    BORDER_CORNER = chr(9562)
    BORDER_BOTTOM = chr(9552)
    TREE_BRANCH = chr(9492)

    def __init__(self, element, nodes, doc):
        super().__init__(element, nodes, doc)
        self.children = []
        self.register_with_parent()

        # Add this object to the mapping of OIDs to node objects.
        nodes[self.oid] = self

    @property
    def parent(self):
        """Locates the node one level above this one in the project tree."""
        try:
            parent_oid = self.element.attrib[self.parent_attr]

        # Top-level nodes(project) do not have a parent_attr.
        except AttributeError:
            parent = None

        else:
            parent = self.nodes[parent_oid]

        return parent

    def register_with_parent(self):
        """
        Records this object as a child of its parent.

        This record is kept because the XML document does not include
        a simple method to find all children of a given node(row).
        """
        if self.parent is not None:
            self.parent.add_child(self)

    def add_child(self, child):
        """Adds a given node as a child."""
        self.children.append(child)

    def get_path(self):
        """
        Builds a list node names, starting from the root(project), and ending
        at this node.
        """
        path = []

        if self.parent is not None:
            path.extend(self.parent.get_path())

        path.append(self.tree_title)

        return path

    @property
    def tree_title(self):
        """Constructs the string identifying this node in the project tree."""
        items = [self.acronym]
        if self.ref_id is not None:
            items.append(self.ref_id)
        items.append(self.name)
        return ' '.join(items)

    @property
    def ref_id(self):
        """
        Creates the identifier shown in square brackets, if the node defined
        a non-emtpy reference identifier.
        """
        try:
            id = self.element.attrib['equipmentid']
        except KeyError:
            id = ''
        return "[{0}]".format(id) if len(id) > 0 else None

    @property
    def name(self):
        """
        Returns the defined name of this node. Subclasses may override this
        for nodes which are named by other means.
        """
        return self.element.attrib['name']

    def path_str(self):
        """Generates a string depicting this node's position in the project."""
        path = self.get_path()
        lines = []
        for i in range(len(path)):
            fields = [self.BORDER_LEFT, ' ']
            fields.append(' ' * i) # Add indentation.

            # Add a tree branch for every node but the first.
            if i:
                fields.append(self.TREE_BRANCH)

            fields.append(path[i]) # Add node path(acronym & name).

            lines.append(''.join(fields))

        lines.append(''.join((self.BORDER_CORNER, self.BORDER_BOTTOM * 80)))

        return '\n'.join(lines)

    def __str__(self):
        """
        Builds a string containing the all the content for this node and
        all children.
        """
        lines = []

        # Include content for this node only if it has any defined tabs,
        # i.e., some node types are structural only and don't have any content
        # of their own.
        if self.tabs:
            lines.append(self.get_content())

        # Recursively include child content.
        lines.extend([str(child) for child in self.children])

        return '\n\n\n'.join(lines)

    def get_content(self):
        """
        Generates a string containing all the content immediately associated
        with this node, beginning with the node's project tree title block
        and followed with all tabs.
        """
        lines = []

        lines.append(self.path_str())
        lines.append(self.get_tab_content())

        return '\n'.join(lines)

    def get_tab_content(self):
        """Generates a string containing content output by all tabs."""
        instances = [t(self.element, self.nodes, self.doc) for t in self.tabs]
        content = [str(i) for i in instances]
        return '\n\n'.join(content)


class Tab(Base):
    """Container for a set of related fields.

    Instance of this object correlates directly with one of the tabs in the
    SISTEMA GUI, containing a set of related parameters, such as
    Documentation or MTTFD.
    """

    # Define a named-tuple to hold the various properties defining a field
    # displaying a single parameter.
    field_names = [
        # The title is the text string describing the parameter; typically
        # matching the text shown in SISTEMA. This can be None if the field
        # doesn't have a title.
        'title',

        # This can be one of the following based on how the parameter value
        # is acquired:
        #
        # 1. A string containing the name of an XML attribute in the parent
        #    node's element.
        #
        # 2. A string containing the name of a method for cases where the
        #    value is not derived from a single attribute.
        #
        # These are attempted in the order listed, i.e., if the XML attribute
        # exists, it will take priority over a method name.
        'attrib',

        # Optional string to identify a property to selectively exclude the
        # field.
        'show'
    ]

    Field = collections.namedtuple('Field', field_names, defaults=[None])

    # Unicode characters used to draw the title box.
    BORDER_LEFT = chr(9474)
    BORDER_CORNER = chr(9492)
    BORDER_BOTTOM = chr(9472)

    # Translations for PL values other than the normal a-e.
    pl_other = {
        'plN': '-',
        'plU': 'n.a.'
    }

    @property
    def parent(self):
        """Acquires the Node object owning this tab."""
        return self.nodes[self.element.attrib['oid']]

    def __str__(self):
        """Generates all output associated with this tab."""
        lines = []

        # Add title.
        lines.append(' '.join((self.BORDER_LEFT, type(self).__name__)))
        lines.append(''.join((self.BORDER_CORNER, self.BORDER_BOTTOM * 40)))

        # Add fields.
        lines.append(self.get_field_content())

        return '\n'.join(lines)

    def get_field_content(self):
        """Generates a string containing the content from all fields."""
        lines = []

        # Translate the raw tuples into Field named-tuples, making
        # identifying each item easier and supplying default values.
        instances = [self.Field(*f) for f in self.fields]

        for field in [i for i in instances if self.show_field(i)]:
            value = self.field_value(field.attrib)

            if field.title:
                lines.append("{0}: {1}".format(field.title, value))
            else:
                lines.append(value)

        return '\n'.join(lines)

    def show_field(self, field):
        """Determines if a field should be output.

        This is based on two conditions:

        1. The field's attrib must name an existing source XML element
           attribute or a method from which the value can be sourced.

        2. If the field contains a show, the property identified by that
           string returns True.
        """
        # Check if the given attribute or value method exists.
        try:
            self.element.attrib[field.attrib]
            exists = True
        except KeyError:
            exists = hasattr(self, field.attrib)

        # Check the show property, defaulting to include the content if
        # a property was not defined.
        if field.show is None:
            show = True
        else:
            show = getattr(self, field.show)

        return exists and show

    def field_value(self, attrib):
        """Acquires the string to be printed as the field's value.

        The attribute's raw value or method return value is output by
        default. The value can be altered if the instance defines a
        format_<attrib> method, in which case the return value is used
        as the output string.
        """
        # See if the XML attribute exists.
        try:
            raw_value = self.element.attrib[attrib]

        # Revert to a method if the XML attribute does not exist.
        except KeyError:
            method = getattr(self, attrib)
            raw_value = method()

        try:
            formatter = getattr(self, '_'.join(('format', attrib)))

        except AttributeError:
            value = raw_value

        else:
            value = formatter(raw_value)

        return value

    def format_pl(self, raw):
        """Formats a PL attribute value.

        This is not direcly called as a field formatting method because
        there are no attributes that are just 'pl'; this is used by actual
        formatting methods that need to normalize PL values.
        """
        # First, see if it's one of the non-alpha values.
        try:
            pl = self.pl_other[raw]

        # Normal PL values strip the 'pl' prefix and convert to lower-case.
        except KeyError:
            pl = raw[-1].lower()

        return pl

    def int_to_bool(self, s):
        """
        Converter method for checkbox parameters which are stored as
        integer attributes: 0 or 1. The given argument can be either
        an attribute name or the raw value.
        """
        # Use an attribute if it exists.
        try:
            i = int(self.element.attrib[s])

        # Otherwise, convert the given value directly.
        except KeyError:
            i = int(s)

        return i > 0

    def csv_to_int(self, csv):
        """
        Converter method to handle values which consist of a comma-separated
        list of integer options, where the integer is the final two characters
        in each option. This method strips the prefix, and converts each
        option to its equivalent integer.
        """
        try:
            return [int(opt.strip()[-2:]) for opt in csv.split(',')]

        # Handle an empty csv strig where split() returns a list containing
        # an empty string.
        except ValueError:
            return []

    def percent(self, s):
        """
        Converts a string representing a floating-point value, typically 0-1,
        into a percentage.
        """
        return str(float(s) * 100)

    def format_cat(self, raw):
        """Formatter for category fields."""
        value = raw[-1]
        if value == 'N':
            value = 'Unknown'
        return value

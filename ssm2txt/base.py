"""
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

    def show(self):
        """Filter function to omit content.

        This object's content will not be sent to the output if this
        method returns False.

        Subclasses may override this to dynamically exclude certain types
        of content, such as when SISTEMA alters the available fields based
        on some parameter.
        """
        return True


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
        nodes[element.attrib['oid']] = self

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
        lines.extend([str(child) for child in self.children if child.show])

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
        content = [str(i) for i in instances if i.show()]
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

        # Associated XML attribute.
        'attrib',

        # Optional string to identify a method to selectively exclude the field.
        'show'
    ]

    Field = collections.namedtuple('Field', field_names, defaults=[None])

    # Unicode characters used to draw the title box.
    BORDER_LEFT = chr(9474)
    BORDER_CORNER = chr(9492)
    BORDER_BOTTOM = chr(9472)

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
        """
        Determines if a field should be output based on the show member
        in the field's definition.
        """
        # Default to True if the show member was omitted.
        if field.show is None:
            show = True

        # If a show member exists, locate the filter method with the same
        # name and call it to determine if the field is output.
        else:
            method = getattr(self, field.show)
            show = method()

        return show

    def field_value(self, attrib):
        """Acquires the string to be printed as the field's value.

        The attribute's raw value is output by default. The value can be
        altered if the instance defines a format_<attrib> method, in which
        case the return value is used as the output string.
        """
        raw_value = self.element.attrib[attrib]

        try:
            formatter = getattr(self, '_'.join(('format', attrib)))

        except AttributeError:
            value = raw_value

        else:
            value = formatter(raw_value)

        return value

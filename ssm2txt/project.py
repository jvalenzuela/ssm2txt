"""
This module defines objects which output content related to the top-level
project node.
"""


from ssm2txt.base import (Node, Tab)


class Documentation(Tab):
    """The project's Documentation tab."""

    title = 'Documentation'
    fields = [
        ('Project name', 'name'),
        ('Creation date', 'createdate'),
        ('Home folder for standards', 'standardsfolder'),
        ('Home folder for documents', 'documentsfolder'),
        ('Project status', 'status'),
        ('Project number', 'number'),
        ('Project version', 'version'),
        ('Authors', 'author'),
        ('Project managers', 'manager'),
        ('Inspectors', 'tester'),
        ('Dangerous point/machine', 'machinename'),
        ('Documentation', 'documentation'),
        ('Document', 'document')
    ]


class Project(Node):
    """The project node itself."""

    acronym = 'PR'
    tabs = [Documentation]

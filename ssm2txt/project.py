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

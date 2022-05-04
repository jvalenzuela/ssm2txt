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

This module defines objects to output content associated with safety function
tree nodes.
"""


from ssm2txt.base import (Node, Tab)


class Documentation(Tab):
    """Output for the Documentation tab."""

    fields = [
        ('Name of safety function', 'name'),
        ('Type of safety function', 'sftype'),
        ('Triggering event', 'triggerevent'),
        ('Reaction and Behaviour on power failure', 'reaction'),
        ('Safe state', 'safestate'),
        ('Operation mode', 'opmode'),
        ('Demand rate', 'requestfrequency'),
        ('Running-on time', 'responsetime'),
        ('Priority', 'priority'),
        ('Documentation', 'documentation'),
        ('Document', 'document')
    ]


class PLr(Tab):
    """Output for the PLr tab."""

    fields = [
        (None, 'plrdet'),

        # Fields for direct PLr entry.
        ('Required Performance Level', 'plr'),
        ('Documentation', 'plrdocumentation'),
        ('Document', 'plrdocument'),
        ('Source', 'plrstandard'),
        ('File', 'plrstandardfile'),

        # Fields for PLr risk graph.
        ('Severity of injury', 'riskparams'),
        ('Frequency and/or exposure times to hazard', 'riskparamf'),
        ('Possibility of avoiding hazard or limiting harm', 'riskparamp'),
        ('Documentation', 'plrgraphdocumentation'),
        ('Document', 'plrgraphdocument')
    ]

    # Translations for the PLr determination selection.
    det_selections = {
        'detMeasures': 'Determine PLr value from risk graph',
        'detDirect': 'Enter PLr value directly'
    }

    # Translations for the risk graph parameters.
    risk_params = {
        '0': '2',
        '1': '1'
        }

    def format_plrdet(self, value):
        """Formatting function for the determination method selection."""
        return self.det_selections[value]

    def format_plr(self, value):
        """Formatting function for the PLr parameter."""
        return self.format_pl(value)

    def format_riskparams(self, value):
        """Formatting function for the severity risk parameter."""
        return ''.join(('S', self.risk_params[value]))

    def format_riskparamf(self, value):
        """Formatting function for the frequency risk parameter."""
        return ''.join(('F', self.risk_params[value]))

    def format_riskparamp(self, value):
        """Formatting function for the avoidance possibility risk parameter."""
        return ''.join(('P', self.risk_params[value]))


class SafetyFunction(Node):
    """Generates output for safety function tree nodes."""

    acronym = 'SF'
    parent_attr = 'projectopoid'
    tabs = [Documentation, PLr]

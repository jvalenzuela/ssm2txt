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

This module defines the class for generating output for the DC tab in blocks
and elements.
"""


from ssm2txt.base import Tab


class DC(Tab):

    fields = [
        (None, 'dcdet'),

        # Fields applicable only when direct DC entry is selected.
        ('Diagnostic coverage', 'dc'),
        ('Documentation', 'dcdocumentation'),

        # Fields applicable only when applied measures is selected.
        (None, 'dcmeasureopoid'),
        ('Documentation', 'dcmeasuredocumentation')
    ]

    methods = {
        'detSubItems': 'Determine DC value from elements',
        'detDirect': 'Enter DC value directly',
        'detMeasures': 'Select applied measures to evaluate DC'
    }

    def format_dcdet(self, value):
        """Formatter for the determination method selection."""
        return self.methods[value]

    def format_dcmeasureopoid(self, oid):
        """Generates a set of fields associated with an applied measure.

        The node'e element does not directly contain this information, but
        rather the source attribute contains an OID referencing the
        element defining the applied measure.
        """
        lines = []
        measure = self.get_measure_element(oid)
        lines.append(' '.join(('Type of measure:',
                               measure.attrib['heading'])))
        lines.append(' '.join(('Description of measure:',
                               measure.attrib['description'])))

        lines.append(self.measures_dc('DC selection from', measure, 'dcmin'))
        lines.append(self.measures_dc('DC selection to', measure, 'dcmax'))
        lines.append(self.measures_dc('Diagnostic coverage', measure, 'dc'))

        pls = self.insufficient_pl(measure)
        lines.append("Measure insufficient for PL: {0}".format(pls))

        return '\n'.join(lines)

    def get_measure_element(self, oid):
        """Locates the element defining the selected DC measure."""
        path = "tables/table/rows/row[@oid='{0}']".format(oid)
        return self.doc.find(path)

    def measures_dc(self, title, element, attrib):
        """Generates a DC percentage field from a measure attribute."""
        return "{0}: {1}".format(title, self.percent(element.attrib[attrib]))

    def insufficient_pl(self, measure):
        """
        Converts the insufficient PLs attribute to a comma-separated
        list of performance levels.
        """
        try:
            pls = [self.format_pl(pl)
                   for pl in measure.attrib['insufficientpls'].split(',')]

        # Handle an empty source string case where split returns a list
        # with an empty string instead of an empty list.
        except IndexError:
            pls = []

        return ', '.join(pls)

    def format_dc(self, raw):
        """Formatter for the Diagnostic coverage field."""
        return self.percent(raw)

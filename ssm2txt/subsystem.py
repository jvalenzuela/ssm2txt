"""
This module defines the set of classes which generate documentation at the
subsystem level of the project tree.
"""


from ssm2txt.base import (Node, Tab)
import ssm2txt.doc as doc
import ssm2txt.mttfd as mttfd


class Documentation(doc.Documentation):
    """The Documentation tab."""

    @property
    def show_cat(self):
        """
        Exclude the Category field; subsystems have a dedicated tab for this
        field.
        """
        return False


class PL(Tab):
    """The subsystem PL tab."""

    fields = [
        (None, 'pldet'),
        ('Performance Level', 'pl'),
        ('Safety Integrity Level', 'sil'),
        ('PL/SIL linked to PFHD', 'isplpfhbind'),
        ('PFHD', 'pfh'),
        (None, 'plconditions'),
        ('Software suitable up to PL', 'pldirectsoftware'),
        ('Documentation', 'pldocumentation'),
        ('Mission time', 'missiontime')
    ]

    # Mapping for the PL determination method selection.
    methods = {
        'detDirect': 'Enter PL/PFHD directly',
        'detSILDirect': 'Enter SIL/PFHD directly',
        'detSubItems': 'Determine PL/PFHD from Category, MTTFD and DCavg',
        'detSubItemsSimple': 'Determine PL/PFHD from Category and DCavg',
    }

    # Mapping for the PLReqXX conditions to their respective text, keyed by
    # the lasted two characters converted to an integer.
    conditions = {
        1: 'Behaviour of the safety function under fault conditions',
        2: 'safety-related software according to clause 4.6 or no software included',
        3: 'systematic failure',
        4: 'Ability to perform a safety function under expected environmental conditions',
        5: 'subsystem is the output part of the SRP/CS',
        6: 'subsystem consists of mechanical, hydraulic or pneumatic components',
        7: 'no application-specific reliability data are available for the components'
    }

    def format_pldet(self, value):
        """Formatting method for the selected method to determine PL."""
        return self.methods[value]

    def format_isplpfhbind(self, raw):
        """Formatting method for the SIL/PL-PFHD checkbox."""
        return str(self.pfhd_linked)

    def format_pldirectsoftware(self, raw):
        """Formatting method for the software PL."""
        return self.format_pl(raw)

    def format_plconditions(self, value):
        """
        Formatting function for the checklist of conditions when PL or SIL is
        not entered directly.
        """
        keys = self.csv_to_int(value)
        return '\n'.join([self.conditions[k] for k in keys])

    def pl(self):
        """
        Generates the performance level, which is sourced from different
        attributes based on the PL/PFHD link option.
        """
        attrib = 'pldirectbindcal' if self.pfhd_linked else 'pldirectnobind'
        raw = self.element.attrib[attrib]
        return self.format_pl(raw)

    def sil(self):
        """
        Generates the SIL value, which is sourced from different attributes
        based on the SIL/PFHD link option.
        """
        attrib = 'sildirectbindcal' if self.pfhd_linked else 'sildirectnobind'

        # Strip the 'sil' prefix.
        raw = self.element.attrib[attrib][-1]

        # Convert the non-numeric option to '-'.
        value = '-' if raw == 'N' else raw

        return value

    @property
    def pfhd_linked(self):
        """Returns the state of the checkbox linking SIL/PL to PFHD."""
        return self.int_to_bool('isplpfhbind')


class Category(Tab):
    """The subsystem Category tab."""

    fields = [
        ('Category of subsystem', 'cat'),
        ('Reduced test frequency', 'reducedtestingrate'),
        ('Requirements for the category', 'catconditions'),
        ('Documentation', 'catdocumentation'),
        ('Source', 'catstandard'),
        ('File', 'catstandardfile')
    ]

    # Mapping from the CATReqXX requirements to their respective text, keyed
    # by the numeric suffix, e.g. CATReq06 is 6.
    requirements = {
        1: 'Basic safety principles are being used.',
        2: 'Well-tried components are being used.',
        3: 'Well-tried safety principles are being used.',
        4: 'A single fault tolerance and reasonable fault detection are given.',
        5: 'Accumulation of faults does not lead to a loss of the safety function.',
        6: 'The requirements for the test frequency are satisfied.',
        10: 'Accordance with relevant standards to withstand the expected influences.'
    }

    def format_reducedtestingrate(self, raw):
        """Formatter for the reduced test frequency checkbox parameter."""
        return str(self.int_to_bool(raw))

    def format_catconditions(self, raw):
        """Formatter for the category requirements checklist."""
        keys = self.csv_to_int(raw)

        # Start with an empty line so the first item begins on the line
        # following the field title.
        lines = ['']

        # Convert the option keys to their relevant strings.
        lines.extend([self.requirements[k] for k in keys])

        return '\n'.join(lines)


class MTTFD(mttfd.MTTFD):
    """The subsystem MTTFD tab."""

    child_type = 'blocks'


class DCavg(Tab):
    """The subsystem DCavg tab."""

    fields = [
        (None, 'dcavgdet'),
        ('Diagnostic coverage', 'dcavg'),
        ('Documentation', 'dcavgdocumentation')
    ]

    det_methods = {
        'detSubItems': 'Determine DCavg value from blocks',
        'detDirect': 'Enter DCavg value directly'
        }

    def format_dcavgdet(self, raw):
        """Formatter for the DCavg method selection."""
        return self.det_methods[raw]

    def format_dcavg(self, raw):
        """Formatter for the diagnostic coverage parameter."""
        return self.percent(raw)


class CCF(Tab):
    """The subsystem CCF tab."""

    fields = [
        (None, 'ccfscoredet'),
        (None, 'list_measures'),
        ('Total points', 'ccfscore'),
        ('Documentation', 'ccfdocumentation'),
        ('Document', 'ccfdocument')
    ]

    # Mapping for the types of CCF evaluation.
    detect = {
        'detMeasures': 'Select applied measures to evaluate CCF',
        'detDirect': 'Enter CCF evaluation directly'
    }

    def format_ccfscoredet(self, value):
        """Formatter for the CCF method selection."""
        return self.detect[value]

    def list_measures(self):
        """Generates the list of applied measures.

        These items are not in the subsystem element, but come from the
        ccfmeasureops table.
        """
        lines = []
        fields = [
            ('Type', 'heading'),
            ('Measure', 'description'),
            ('Points', 'score')
        ]
        for e in self.get_measures_elements():
            lines.extend([": ".join((title, e.attrib[attrib]))
                          for title, attrib in fields])
        return '\n'.join(lines)

    def get_measures_elements(self):
        """
        Acquires the list of rows in the ccfmeasureops table that point
        back to this node via the componentopoid attribute.
        """
        path = "tables/table[@table_name='ccfmeasureops']/" \
            "rows/row[@componentopoid='{0}']".format(self.parent.oid)
        return self.doc.findall(path)


class Subsystem(Node):
    """Generates output for subsystem nodes of the project tree."""

    acronym = 'SB'
    parent_attr = 'sfopoid'
    tabs = [Documentation, PL, Category, MTTFD, DCavg, CCF]

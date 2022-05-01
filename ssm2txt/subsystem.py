"""
This module defines the set of classes which generate documentation at the
subsystem level of the project tree.
"""


from ssm2txt.base import (Node, Tab)
from ssm2txt.doc import Documentation
import ssm2txt.mttfd as mttfd


class PL(Tab):
    """The subsystem PL tab."""

    fields = [
        (None, 'pldet'),
        ('Performance Level', 'pl', 'show_pl'),
        ('Safety Integrity Level', 'sil', 'show_sil'),
        ('PL/SIL linked to PFHD', 'isplpfhbind', 'show_common_direct'),
        ('PFHD', 'pfh', 'show_common_direct'),
        (None, 'plconditions', 'show_plconditions'),
        ('Software suitable up to PL', 'pldirectsoftware', 'show_software'),
        ('Documentation', 'pldocumentation'),
        ('Mission time', 'missiontime', 'show_common_direct')
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

    def show_pl(self):
        """Filter function to enable fields unique to direct PL entry."""
        return self.element.attrib['pldet'] == 'detDirect'

    def show_sil(self):
        """Filter function to enable fields unique to direct SIL entry."""
        return self.element.attrib['pldet'] == 'detSILDirect'

    def show_common_direct(self):
        """
        Filter function to enable fields common to both direct-entry methods:
        PL and SIL.
        """
        return self.show_pl() or self.show_sil()

    def show_plconditions(self):
        """
        Filter function to enable the list of checked options when not using
        PL/SIL direct entry.
        """
        return self.parent.pl_from_cat or self.parent.pl_from_cat_simple

    def show_software(self):
        """Filter function to enable the software PL field."""
        return self.element.attrib['pldet'] != 'detSubItemsSimple'

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

        The source attribute can contain all available options, even those
        not displayed based on the PL determination method.
        """
        keys = self.csv_to_int(value)

        # Options 5-7 are only applicable if the simplified method is selected.
        limit = 7 if self.parent.pl_from_cat_simple else 4
        filtered_keys = [k for k in keys if k <= limit]

        return '\n'.join([self.conditions[k] for k in filtered_keys])

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
        ('Reduced test frequency', 'reducedtestingrate', 'show_reduced_test'),
        ('Requirements for the category', 'catconditions', 'show_requirements'),
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

    # Mapping to indicate the requirements available for each category. The
    # keys are the same as the requirements dict, and the values are the
    # set of categories which include that requirement.
    req_show = {
        1: 'B1234',
        2: '1',
        3: '1234',
        4: '34',
        5: '4',
        6: '2',
        10: 'B1234'
    }

    def show(self):
        """
        Filter function to hide this tab when PL is determined via direct
        SIL entry.
        """
        return not 'SIL' in self.element.attrib['pldet']

    def show_requirements(self):
        """Filter function to enable the requirements checklist."""
        return self.category != 'Unknown'

    def show_reduced_test(self):
        """Filter function to enable the reduced test frequency parameter."""
        return self.category == '2'

    def format_reducedtestingrate(self, raw):
        """Formatter for the reduced test frequency checkbox parameter."""
        return str(self.int_to_bool(raw))

    def format_catconditions(self, raw):
        """Formatter for the category requirements checklist."""
        keys = self.csv_to_int(raw)

        # Remove options not applicable to the selected category.
        filtered = [k for k in keys if self.category in self.req_show[k]]

        # Start with an empty line so the first item begins on the line
        # following the field title.
        lines = ['']

        # Convert the option keys to their relevant strings.
        lines.extend([self.requirements[k] for k in filtered])

        return '\n'.join(lines)


class MTTFD(mttfd.MTTFD):
    """The subsystem MTTFD tab."""

    child_type = 'blocks'

    def show(self):
        """
        Filter method to enable the MTTFD tab only when PL is determined by
        category, MTTFD, and DCavg.
        """
        return self.parent.pl_from_cat


class DCavg(Tab):
    """The subsystem DCavg tab."""

    fields = [
        (None, 'dcavgdet'),
        ('Diagnostic coverage', 'dcavg', 'show_direct'),
        ('Documentation', 'dcavgdocumentation', 'show_direct')
    ]

    det_methods = {
        'detSubItems': 'Determine DCavg value from blocks',
        'detDirect': 'Enter DCavg value directly'
        }

    def show(self):
        """Filter function to enable this tab."""
        include = True

        # Excluded when direct-entry PL/SIL is used.
        if not (self.parent.pl_from_cat or self.parent.pl_from_cat_simple):
            include = False

        # Excluded for categories B and 1.
        if self.category in 'B1':
            include = False

        # Exclude when PL is determined from subitems and MTTFD is a fault
        # exclusion.
        if self.parent.pl_from_cat and self.parent.mttfd_fault_exclusion:
            include = False;

        return include

    def show_direct(self):
        """Filter to show fields unique to the direct entry method."""
        return self.parent.dcavg_direct

    def format_dcavgdet(self, raw):
        """Formatter for the DCavg method selection."""
        return self.det_methods[raw]


class CCF(Tab):
    """The subsystem CCF tab."""

    fields = [
        (None, 'ccfscoredet'),
        (None, 'list_measures', 'show_measures'),
        ('Total points', 'ccfscore', 'show_direct'),
        ('Documentation', 'ccfdocumentation'),
        ('Document', 'ccfdocument')
    ]

    # Mapping for the types of CCF evaluation.
    detect = {
        'detMeasures': 'Select applied measures to evaluate CCF',
        'detDirect': 'Enter CCF evaluation directly'
    }

    def show(self):
        """Filter function to selectively omit the CCF tab."""
        include = True

        # CCF is omitted if PL/SIL is entered directly.
        if not (self.parent.pl_from_cat or self.parent.pl_from_cat_simple):
            include = False

        # CCF is omitted for categories less than 2.
        if not self.category in '234':
            include = False

        # CCF is omitted if MTTFD is entered directly.
        if self.parent.mttfd_direct and self.parent.mttfd_fault_exclusion:
            include = False

        return include

    def show_measures(self):
        """Filter method to enable the list of applied measures."""
        return self.element.attrib['ccfscoredet'] == 'detMeasures'

    def show_direct(self):
        """Filter method to enable direct CCF entry fields."""
        return self.element.attrib['ccfscoredet'] == 'detDirect'

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

    @property
    def show_children(self):
        """Excludes child nodes when MTTFD and DCavg are directly entered."""
        return not self.mttfd_direct or not self.dcavg_direct

    @property
    def pl_from_cat(self):
        """True if PL is determined from category, MTTFD, and DCavg."""
        return self.element.attrib['pldet'] == 'detSubItems'

    @property
    def pl_from_cat_simple(self):
        """
        True if PL is determined from category and DCavg, using the
        simplified method.
        """
        return self.element.attrib['pldet'] == 'detSubItemsSimple'

    @property
    def dcavg_direct(self):
        """Logical state of the DCavg direct entry selection."""
        return self.element.attrib['dcavgdet'] == 'detDirect'

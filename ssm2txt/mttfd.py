"""
This module defines the MTTFD tab applicable to subsystems, blocks, and
elements.
"""


from ssm2txt.base import Tab


class MTTFD(Tab):

    fields = [
        (None, 'mttfddet'),
        ('MTTFD', 'mttfd', 'show_mttfd'),
        ('Fault exclusion', 'fault_exclusion', 'show_direct'),

        # Fields enabled when using B10D/B10.
        ('B10D', 'b10d', 'show_b10d'),
        ('B10', 'b10', 'show_b10'),
        ('RDF', 'rdfb10', 'show_b10'),
        ('nop', 'nop', 'show_nop'),
        ('d_op', 'nopday', 'show_nop'),
        ('h_op', 'nophour', 'show_nop'),
        ('t_cycle', 'nopcycle', 'show_nop'),

        # Fields enabled when using Lambda/MTTF/MTBF/RDF.
        ('Lambda', 'lambda', 'show_lambda'),
        ('MTTF', 'mttf', 'show_mttf'),
        ('MTBF', 'mtbf', 'show_mtbf'),
        ('RDF', 'rdfmttf', 'show_rdf_mttf'),

        ('Documentation', 'mttfddocumentation', 'show_doc'),
        ('Mission time', 'missiontime')
    ]

    # Mapping for the MTTFD determination method.
    det_methods = {
        'detSubItems': 'Determine MTTFD value from {0}',
        'detDirect': 'Enter MTTFD value directly',
        'detB10D': 'Determine MTTFD value from B10D/B10 value',
        'detMTTF': 'Determine MTTFD value from Lambda/MTTF/MTBF and RDF value'
        }

    @property
    def determine_with_b10(self):
        """True when MTTFD is calculated from B10D/B10"""
        return self.element.attrib['mttfddet'] == 'detB10D'

    @property
    def determine_with_mttf(self):
        """True when MTTFD is calculated from Lambda/MTTF/MTBF/RDF."""
        return self.element.attrib['mttfddet'] == 'detMTTF'

    def show_mttfd(self):
        """Filter method to enable the MTTFD value."""
        return self.mttfd_direct and not self.mttfd_fault_exclusion

    def show_direct(self):
        """Filter method to enable fields relevant to direct MTTFD entry."""
        return self.mttfd_direct

    def show_b10(self):
        """Filter method to display fields relevant to determination via B10."""
        return (self.determine_with_b10
                and self.element.attrib['calcb10ddet'] == 'calcB10dB10')

    def show_b10d(self):
        """Filter method to display the B10D field."""
        return (self.determine_with_b10
                and self.element.attrib['calcb10ddet'] == 'calcB10dDirect')

    def show_nop(self):
        """Filter method to display fields relevant to B10/B10D nop."""
        return self.determine_with_b10

    def show_rdf_mttf(self):
        """Filter method to display the RDF field associated with MTTF."""
        return self.determine_with_mttf

    def show_lambda(self):
        """Filter method to display the Lambda field."""
        return (self.determine_with_mttf
                and self.element.attrib['calcmttfddet'] == 'calcMTTFdLambda')

    def show_mttf(self):
        """Filter method to display the MTTF field."""
        return (self.determine_with_mttf
                and self.element.attrib['calcmttfddet'] == 'calcMTTFdMTTF')

    def show_mtbf(self):
        """Filter method to display the MTBF field."""
        return (self.determine_with_mttf
                and self.element.attrib['calcmttfddet'] == 'calcMTTFdMTBF')

    def show_doc(self):
        """
        Filter method to omit the Documentation field when MTTFD is determined
        from child nodes.
        """
        return self.element.attrib['mttfddet'] != 'detSubItems'

    def format_mttfddet(self, raw):
        """Formatter for the MTTFD determination method."""
        return self.det_methods[raw].format(self.child_type)

    def format_rdfb10(self, raw):
        """Formatter for the B10 RDF field."""
        return self.format_rdf(raw)

    def format_rdfmttf(self, raw):
        """Formatter for the MTTF RDF field."""
        return self.format_rdf(raw)

    def format_rdf(self, raw):
        """Formatter for all RDF values."""
        return self.percent(raw)

    def fault_exclusion(self):
        """Formatter for the fault exclusion checkbox.

        This is not named per format_<attrib> because the fault exclusion
        option is derived from the same attribute as the MTTFD value.
        """
        return str(self.mttfd_fault_exclusion)

    def format_nop(self, raw):
        """Formatter method for B10/B10D nop field."""
        if float(raw) < 0:
            return 'INF'
        else:
            return raw

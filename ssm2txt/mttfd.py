"""
This module defines the MTTFD tab applicable to subsystems, blocks, and
elements.
"""


from ssm2txt.base import Tab


class MTTFD(Tab):

    fields = [
        (None, 'mttfddet'),
        ('MTTFD', 'mttfd'),
        ('Fault exclusion', 'fault_exclusion_checkbox'),

        # B10D/B10 fields.
        ('Use B10/B10D', 'calcb10ddet'),
        ('B10', 'b10'),
        ('B10D', 'b10d'),
        ('B10 RDF', 'rdfb10'),
        ('nop', 'nop'),
        ('d_op', 'nopday'),
        ('h_op', 'nophour'),
        ('t_cycle', 'nopcycle'),

        # Lambda/MTTF/MTBF/RDF fields.
        ('Use Lambda/MTTF/MTBF', 'calcmttfddet'),
        ('Lambda', 'lambda'),
        ('MTTF', 'mttf'),
        ('MTBF', 'mtbf'),
        ('Lambda/MTTF/MTBF RDF', 'rdfmttf'),

        ('Documentation', 'mttfddocumentation'),
        ('Mission time', 'missiontime')
    ]

    # Mapping for the MTTFD determination method.
    det_methods = {
        'detSubItems': 'Determine MTTFD value from {0}',
        'detDirect': 'Enter MTTFD value directly',
        'detB10D': 'Determine MTTFD value from B10D/B10 value',
        'detMTTF': 'Determine MTTFD value from Lambda/MTTF/MTBF and RDF value'
        }

    # Mapping for the B10/B10D pull-down option.
    b10_options = {
        'calcB10dB10': 'B10',
        'calcB10dDirect': 'B10D'
        }

    def format_mttfddet(self, raw):
        """Formatter for the MTTFD determination method."""
        return self.det_methods[raw].format(self.child_type)

    def format_mttfd(self, raw):
        """Formmater for the MTTFD field."""
        return 'FE' if self.fault_exclusion else raw

    def format_calcb10ddet(self, raw):
        """
        Formatter for the B10/B10D selection when MTTFD is determined by
        B10/B10D.
        """
        return self.b10_options[raw]

    def format_rdfb10(self, raw):
        """Formatter for the B10 RDF field."""
        return self.format_rdf(raw)

    def format_calcmttfddet(self, raw):
        """Formatter for the Lambda/MTTF/MTBF pull-down selection."""
        return raw[9:] # Strip off the 'calcMTTFd' prefix.

    def format_rdfmttf(self, raw):
        """Formatter for the MTTF RDF field."""
        return self.format_rdf(raw)

    def format_rdf(self, raw):
        """Formatter for all RDF values."""
        return self.percent(raw)

    def fault_exclusion_checkbox(self):
        """Formatter for the fault exclusion checkbox."""
        return str(self.fault_exclusion)

    def format_nop(self, raw):
        """Formatter method for B10/B10D nop field."""
        if float(raw) < 0:
            return 'INF'
        else:
            return raw

    @property
    def fault_exclusion(self):
        """Logical state of the fault exclusion checkbox.

        This field doesn't have a dedicated attribute, but is derived from
        the mttfd value.
        """
        return float(self.element.attrib['mttfd']) < 0

import argparse
import os.path
import xml.etree.ElementTree as ElementTree
from ssm2txt.project import Project
from ssm2txt.sf import SafetyFunction
from ssm2txt.subsystem import Subsystem
from ssm2txt.channel import Channel
from ssm2txt.block import Block
from ssm2txt.element import Element


def get_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(prog='ssm2txt',
                                     description='SISTEMA to text converter.')
    parser.add_argument('ssm', help='Source SISTEMA project file')
    return parser.parse_args()


class SSM(object):
    """
    This object handles all the processing for a given ssm project file to
    generate the output text file.
    """

    # Mapping of table_name attribute to the type of Node object that will
    # be instantiated for each row.
    tables = {
        'projectops': Project,
        'sfops': SafetyFunction,
        'componentops': Subsystem,
        'channelops': Channel,
        'blocops': Block,
        'elementops': Element
    }

    def __init__(self, filename):
        self.filename = filename
        doc = self.parse()
        nodes = self.read_tables(doc)
        self.prj = self.get_project(doc, nodes)

    def parse(self):
        """Reads the ssm XML into an ElementTree document."""
        tree = ElementTree.parse(self.filename)
        return tree.getroot()

    def read_tables(self, doc):
        """Loads all tables within the source document."""
        # This is a mapping from OID to the object instantiated for the
        # given XML element.
        nodes = {}

        for table in doc.iterfind('tables/table'):
            try:
                row_type = self.tables[table.attrib['table_name']]

            # Ignore tables that don't have an assigned row object type.
            except KeyError:
                continue

            self.read_nodes(table, row_type, nodes, doc)

        return nodes

    def read_nodes(self, table, row_type, nodes, doc):
        """Instantiates objects for rows in a given table."""
        [row_type(row, nodes, doc) for row in table.iterfind('rows/*')]

    def get_project(self, doc, nodes):
        """
        Locates the project object, which is the object associated with
        the first, and only row in the projectops table.
        """
        element = doc.find("tables/table[@table_name='projectops']/rows/row")
        return nodes[element.attrib['oid']]

    def __str__(self):
        """Returns the output content acquired from the source ssm project."""
        return str(self.prj)

    def write(self):
        """Writes the content to the output file."""
        with open(self.output_filename, 'w', encoding='utf_8') as f:
            f.write(str(self))

    @property
    def output_filename(self):
        """Generates the output filename based on the source filename.

        The target filename is the same as the source .ssm file, with
        the extension changed to .txt.
        """
        root = os.path.splitext(self.filename)[0]
        return '.'.join((root, 'txt'))


args = get_args()
ssm = SSM(args.ssm)
ssm.write()

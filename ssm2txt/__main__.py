import argparse
import xml.etree.ElementTree as ElementTree


def get_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(prog='ssm2txt',
                                     description='SISTEMA to text converter.')
    parser.add_argument('ssm', help='Source SISTEMA project file')
    return parser.parse_args()


def parse_xml(filename):
    """Reads the ssm XML into an ElementTree document."""
    tree = ElementTree.parse(filename)
    return tree.getroot()


args = get_args()
doc = parse_xml(args.ssm)

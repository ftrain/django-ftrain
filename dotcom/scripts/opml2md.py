#!/usr/bin/env python
# Using code from http://www.artima.com/weblogs/viewpost.jsp?thread=4829

import xml.etree.ElementTree as ET 

import sys
import getopt

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def opml_to_html(tree):
    pass

def opml_to_markdown(tree):
    body = tree.find('body')
    string = []
    for out in body.findall('outline'):
        string.append("\n\n## " + out.attrib['title'])
        for link in out.findall('outline'):
            string.append('- [%s](%s) [+](%s)' % 
                          ( link.attrib['title'].encode('utf-8'), 
                            link.attrib['htmlUrl'], 
                            link.attrib['xmlUrl'] ))
    return string.join("\n")

def main(argv=None):
    """
    Taking an OPML file go through it and create a simple
    markdown list of all feeds.
    """
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)

        file_name = args[0]
        tree = ET.parse(file_name)
        print opml_to_markdown(tree)

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "For help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())

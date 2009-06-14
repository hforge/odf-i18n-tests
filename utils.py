# -*- coding: UTF-8 -*-
# Copyright (C) 2008 Sylvain Taverne <sylvain@itaapy.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Import from the Standard Library
from operator import attrgetter
from difflib import ndiff
from re import compile
from sys import stderr, stdout

# Import from itools
from itools.handlers import get_handler
from itools.odf.odf import ODFFile
from itools.uri import get_uri_path, resolve_uri
from itools import vfs


def get_tests():
    """Returns list of tuples:

        [(odf_path, po_handler), ...]
    """
    # We traverse all ODF documents
    for odf_uri in vfs.traverse('./documents/'):
        odf_handler = get_handler(odf_uri)
        if not isinstance(odf_handler, ODFFile):
            continue
        # We found a ODF Document, We search the corresponding PO file
        po_uri = resolve_uri(odf_uri, 'testDoc.po')
        yield get_uri_path(odf_uri), get_handler(po_uri)



def progress(current, total):
    """Permit to calculate the work progression.
    """
    status = current*50/total
    str = '\r[%s>%s] %d/%d' %((status-1)*'=', (50-status)*' ', current, total)
    stdout.write(str)



def write_diff_file(test_number, diff_filename, odf_uri, po_uri, odf_sources,
                    po_sources):
    """Write a diff file which summarize the failure of a specific test.
    """
    # Create or open the diff file
    diff_file_path = 'results/%s' % diff_filename
    diff_file = vfs.make_file(diff_file_path)

    # Write the header
    diff_file.write(25*'=' + 'Test %d FAILED' %test_number + 25*'=' + '\n')
    diff_file.write('INPUT:  ' + str(odf_uri) + '\n')
    diff_file.write('OUTPUT: ' + str(po_uri) + '\n\n')
    diff_file.write(
        "The '-' sign correspond to a line that is expected but don't "
        "appears well or not at all after the extraction.\n"
        "The '+' sign correspond to a line that appears after the extraction "
        "but is not expected.\n")
    diff_file.write(25*'=' + 'Test %d FAILED' %test_number + 25*'=' + '\n')

    # Write the diff summary
    for line in ndiff(po_sources, odf_sources):
        diff_file.write(line.encode('utf-8') + '\n')
    diff_file.close()


def clean_sources(sources, re_tags=compile('<.*?>')):
    return [ re_tags.sub('', x) for x in sources ]


def start_test(odf_handler):
    # Create the 'results' folder
    if vfs.exists('results'):
        vfs.remove('results')
    vfs.make_folder('results')

    # Find test files
    print 'Searching for ODF files...'
    unitests = get_tests()
    unitests = list(unitests)
    nb_tests = len(unitests)
    print 'Number of files found: %d' % nb_tests

    test_number = 0
    msgs_error = []
    for odf_path, po_handler in unitests:
        # Progress bar
        test_number += 1
        progress(test_number, nb_tests)

        # Call ODF handler
        try:
            odf_sources = odf_handler(odf_path)
        except:
            print 'ERROR with test %d / "%s"' % (test_number, odf_path)
            continue

        # Post-process the results
        odf_sources = clean_sources(odf_sources)
        odf_sources = list(set(odf_sources)) # Remove duplicates
        odf_sources.sort()
        # Expected results
        po_sources = [ u''.join(x.source) for x in po_handler.get_units() ]
        po_sources = clean_sources(po_sources)
        po_sources.sort()
        # Check
        if odf_sources == po_sources:
            continue

        # Error. Create a diff report for the current test.
        test_name = odf_path.split('/')[-2]
        filename = 'test_%d_%s.txt' % (test_number, test_name)
        po_path = get_uri_path(po_handler.uri)
        write_diff_file(test_number, filename, odf_path, po_path, odf_sources,
                        po_sources)
        # Inform the user that there where failures
        msgs_error.append('results/%s\n' % filename)

    # Summurarizes the results
    print
    print 'Results:'
    print '--------'
    print '    %s Tests' % nb_tests
    print '    %s Errors' % len(msgs_error)
    print
    if msgs_error:
        stderr.write('Generated error files\n')
        stderr.write('---------------------\n')
        for msg in msgs_error:
            stderr.write(msg)


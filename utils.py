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
from sys import stderr

# Import from itools
from itools.handlers import get_handler
from itools.odf import ODTFile, ODPFile, ODSFile
from itools.vfs import vfs, exists, is_folder, is_file, make_folder, make_file


def get_tests():
    """Return list of tuple
      [(odf_filename1, po_handler1),
       (odf_filename2, po_handler2),
        ...]
    """
    result = []
    # We traverse all ODF documents
    for handler in vfs.traverse('./documents/'):
        handler = get_handler(handler.path)
        is_odf_document = isinstance(handler, (ODTFile, ODPFile, ODSFile))
        if not is_odf_document:
            continue
        # We found a ODF Document, We search the corresponding PO file
        po_uri = handler.uri.resolve('%s.po' % 'testDoc')
        po_handler = get_handler(po_uri)
        result.append((str(handler.uri.path), po_handler))
    return result



def progress(current, total, file_descriptor=stderr):
    """Permit to calculate the work progression."""
    status = current*50/total
    str = '\r[%s>%s] %d/%d' %((status-1)*'=', (50-status)*' ', current, total)
    file_descriptor.write(str)



def get_test_name(odf_uri, test_number):
    """Return some informations."""
    test_name = str(odf_uri).split('/')[-2]
    file_name = 'test_%d_%s.txt' % (test_number, test_name)
    return test_name, file_name



def write_diff_file(test_infos, test_number):
    """Write a diff file which summarize the failure of a specific test."""
    diff_file_name, uris, sources = test_infos
    odf_uri, po_uri = uris
    odf_sources, po_sources = sources

    # Create or open the diff file
    diff_file_path = 'results/%s' % diff_file_name
    if exists(diff_file_path) and is_file(diff_file_path):
        diff_file = open(diff_file_path, 'w')
    else:
        diff_file = make_file(diff_file_path)

    # Write the header
    diff_file.write(25*'=' + 'Test %d FAILED' %test_number + 25*'=' + '\n')
    diff_file.write('INPUT:  ' + str(odf_uri) + '\n')
    diff_file.write('OUTPUT: ' + str(po_uri) + '\n\n')
    diff_file.write(
        "The '-' sign correspond to a line that is expected but don't "
        "appears well or not at all after the extraction.\n"
        "The '+' sign correcpond to a line that appears after the extraction "
        "but is not expected.\n")
    diff_file.write(25*'=' + 'Test %d FAILED' %test_number + 25*'=' + '\n')

    # Write the diff summary
    for line in ndiff(po_sources, odf_sources):
        diff_file.write(line.encode('utf-8') + '\n')
    diff_file.close()


def clean_sources(sources):
    result = []
    re_tags = compile('<.*?>')
    for source in sources:
        source = re_tags.sub('', source)

        result.append(source)
    return result


def start_test(odf_handler):
    print 'Searching for ODF files...'
    unitests = get_tests()
    nb_tests = len(unitests)
    print 'Number of files found: %d' % nb_tests

    test_number = 0
    nb_errors = 0
    msgs_error = []
    for odf_filename, po_handler in unitests:
        test_number+=1

        # Actualize the progress bar
        progress(test_number, nb_tests)

        # Get sources
        try:
            odf_sources = odf_handler(odf_filename)
        except:
            print 'ERROR with test %d / "%s"' % (test_number,odf_filename)
            continue
        po_sources = [u''.join(unit.source)
                      for unit in po_handler.get_units()]
        odf_sources = clean_sources(odf_sources)
        po_sources = clean_sources(po_sources)

        # Remove the duplicated sources
        odf_sources = list(set(odf_sources))

        # Sort
        odf_sources.sort()
        po_sources.sort()

        # If the output file and expected results are different
        if odf_sources != po_sources:
            if not is_folder('results'):
                make_folder('results')
            nb_errors+=1

            # Create a diff report for the current test
            test_name, file_name = get_test_name(odf_filename, test_number)
            test_infos = [file_name, (odf_filename, po_handler.uri.path),
                          (odf_sources, po_sources)]
            write_diff_file(test_infos, test_number)

            # Inform the user that there where failures
            msgs_error.append('./results/%s has been generated' % file_name)

    # Summurarizes the results
    stderr.write('\n')
    print 'Results:'
    print '--------'
    print '    %s Tests' % nb_tests
    print '    %s Errors' % nb_errors
    if msgs_error:
        print
        print 'Generated error files:'
        print '---------'
        for msg in msgs_error:
            print '    %s' % msg




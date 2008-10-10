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
from sys import stderr

# Import from itools
from itools.vfs import exists, is_folder, is_file, make_folder, make_file
from itools.gettext import POUnit
from itools.gettext.po import encode_source

# Import from odf i18n tests
from utils import get_unitests_handlers


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
        "The '-' sign correspond to a line that is expected but don't appears "
        "well or not at all after the extraction.\n"
        "The '+' sign correcpond to a line that appears after the extraction "
        "but is not expected.\n")
    diff_file.write(25*'=' + 'Test %d FAILED' %test_number + 25*'=' + '\n')

    # Write the diff summary
    for line in ndiff(po_sources, odf_sources):
        diff_file.write(line.encode('utf-8') + '\n')
    diff_file.close()


def get_sources(units):
    result = []
    for unit in units:
        source = u''.join(unit.source)
        # Remove tags
        while True:
            s_cut = source.find('<')
            f_cut = source.find('>', s_cut)
            if s_cut < 0 or f_cut < 0:
                break
            source = source[:s_cut]+source[f_cut+1:]
        result.append(source)
    return result


if __name__ == '__main__':
    print 'Searching for ODF files...'
    unitests_handlers = get_unitests_handlers()
    nb_tests = len(unitests_handlers)
    print 'Number of files found: %d' % nb_tests

    test_number = 0
    nb_errors = 0
    msgs_error = []
    for odf_handler, po_handler in unitests_handlers:
        test_number+=1

        # Actualize the progress bar
        progress(test_number, nb_tests)

        odf_units = []
        for unit, context, references in odf_handler.get_units():
            source = encode_source(unit)
            message = POUnit('', None, [source], [u''])
            odf_units.append(message)
        po_units = po_handler.get_units()

        # Get sources
        odf_sources = get_sources(odf_units)
        po_sources = get_sources(po_units)

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
            test_name, file_name = get_test_name(odf_handler.uri,
                                                 test_number)
            test_infos = [file_name, (odf_handler.uri, po_handler.uri),
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

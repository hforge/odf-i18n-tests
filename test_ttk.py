# -*- coding: UTF-8 -*-
# Copyright (C) 2008 David Versmisse <david.versmisse@itaapy.com>
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

# Import from itools
from subprocess import Popen, PIPE

# Import from itools
from itools.xliff import XLFFile
from itools.vfs import remove
from itools.gettext.po import encode_source

# Import from odf i18n tests
from utils import start_test


def ttk_odf2xliff_handler(filename):
    # Make the xliff file
    process = Popen(['odf2xliff', filename, 'tmp.xlf'],
                    stdout=PIPE, stderr=PIPE)
    if process.wait() != 0:
        raise ValueError, '"%s" is malformed' % filename

    # Get the units
    units = []
    xlf_file = XLFFile('tmp.xlf')
    for a_file in xlf_file.files.values():
        for unit in a_file.body.values():
            units.append(encode_source(unit.source))

    # Remove the tmp file
    remove('tmp.xlf')

    return units


if __name__ == '__main__':
    start_test(ttk_odf2xliff_handler)



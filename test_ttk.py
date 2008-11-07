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
import cStringIO
import zipfile
from string import whitespace

# Import from odf i18n tests
from utils import start_test

# Import from ttk
from translate.storage.xml_extract import extract
from translate.storage import odf_shared
from translate.storage.xliff import xlifffile


def ttk_handler(filename):
    store = xlifffile()

    try:
        z = zipfile.ZipFile(filename, 'r')
        contents = z.read("content.xml")
    except (ValueError, zipfile.BadZipfile):
        contents = open(filename, 'r').read()
    parse_state = extract.ParseState(odf_shared.no_translate_content_elements,
                                     odf_shared.inline_elements)
    extract.build_store(cStringIO.StringIO(contents), store, parse_state)

    result = []
    for unit in store.getunits():
        unit = unit.getsource().strip(whitespace)
        if unit.strip():
            result.append(unit)

    return result


if __name__ == '__main__':
    start_test(ttk_handler)


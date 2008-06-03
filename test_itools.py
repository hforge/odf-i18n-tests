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
from pprint import pprint

# Import from odf i18n tests
from utils import get_unitests_handlers

# Import from itools
from itools.odf import ODTFile, ODPFile, ODSFile

if __name__ == '__main__':
    criterium = attrgetter('msgid')
    unitests_handlers = list(get_unitests_handlers())
    nb_tests = len(unitests_handlers)
    i = 0
    nb_errors = 0
    for odf_handler, po_handler in unitests_handlers:
        i+=1
        odf_messages = sorted(odf_handler.get_messages(), key=criterium)
        po_messages = sorted(po_handler.get_messages(), key=criterium)
        if odf_messages != po_messages:
            nb_errors+=1
            print 25*'='
            print 'Test %d FAILED' % i
            print 25*'='
            print odf_handler.uri
            print po_handler.uri
            print
            pprint(odf_messages)
            print
            print 'Different of:'
            print
            pprint(po_messages)
    print
    print 25*'='
    print 'Results'
    print 25*'='
    print '%s Tests' % nb_tests
    print '%s Errors' % nb_errors
    print 25*'='

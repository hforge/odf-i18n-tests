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
from pprint import pprint, pformat

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
        list_msgid = []
        messages_to_remove = []
        odf_messages = list(odf_handler.get_messages())
        # Remove odf doublons
        for message in odf_messages:
            if message.msgid in list_msgid:
                messages_to_remove.append(message)
            else:
                list_msgid.append(message.msgid);
        for message_to_remove in messages_to_remove:
            odf_messages.remove(message_to_remove)

        odf_messages = sorted(odf_messages, key=criterium)
        po_messages = sorted(po_handler.get_messages(), key=criterium)
        if odf_messages != po_messages:
            nb_errors+=1
            test_name = str(odf_handler.uri).split('/')[-2]
            file_name = 'test_%d_%s.odf.txt' % (i, test_name)
            file_path = './tests_results/%s' % file_name
            odf_results = file(file_path,'w')
            odf_results.write(25*'=')
            odf_results.write('Test %d FAILED' %i)
            odf_results.write(25*'=' + '\n')
            odf_results.write(str(odf_handler.uri) + '\n')
            odf_results.write('')
            odf_results.write(pformat(odf_messages))
            odf_results.close
            print file_name + ' has been generated'
            file_name = 'test_%d_%s.po.txt' % (i, test_name)
            file_path = './tests_results/%s' % file_name
            po_results = file(file_path,'w')
            po_results.write(25*'=')
            po_results.write('Test %d FAILED' %i)
            po_results.write(25*'=' + '\n')
            po_results.write(str(po_handler.uri) + '\n')
            po_results.write('')
            po_results.write(pformat(po_messages))
            po_results.close
            print file_name + ' has been generated'
            print

    print 25*'='
    print 'Results'
    print 25*'='
    print '%s Tests' % nb_tests
    print '%s Errors' % nb_errors
    print 25*'='

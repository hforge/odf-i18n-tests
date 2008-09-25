# -*- coding: UTF-8 -*-
# Copyright (C) 2008 Gautier Hayoun <gautier@itaapy.com>
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
from itools.handlers import Database, ConfigFile, get_handler
from itools.handlers import register_handler_class
from itools.vfs import traverse, open, make_file, exists
from itools.xml import XMLParser, START_ELEMENT, END_ELEMENT, TEXT
import itools.http

# Import from Standard Library
from mimetypes import add_type


def strong_escape(s):
    """ a way to escape string """
    return "\"" + s.replace("\"", "\\\"") + "\""


FELLOWSHIP_PREFIX = 'http://testsuite.opendocumentfellowship.com/testcases/'


if __name__ == '__main__':
    # Open a log file for failed files
    if not exists('error_logs'):
        make_file('error_logs')
    errors = open('error_logs', 'rw')
    # does 'a' flag works ??
    errors.write(errors.read())
    errors.write("# -- Error log --\n")
    errors.write("# Please update those file manually\n")

    # Register ConfigFile to .conf
    ConfigFile.class_mimetypes = ['text/x-setup_conf']
    add_type('text/x-setup_conf', '.conf')
    register_handler_class(ConfigFile)

    db = Database().get_handler('documents')
    count = 0
    # For each test case
    for f in db.traverse():
        if str(f.uri).endswith('setup.conf'):
            # Has to update it
            url = str(f.uri)
            splited = url.split('/')
            i = 0
            for split in splited:
                if split == 'documents':
                    i += 1
                    break
                i += 1
            url = FELLOWSHIP_PREFIX + '/'.join(splited[i:])
            url = url.replace('setup.conf', 'test.xml')

            try:
                data = open(url).read()
            except LookupError:
                msg = "[%d] %s NOT updated\n" % (count, '/'.join(splited[i:]))
                print msg
                errors.write(msg)
                count += 1
                continue


            # Find the original description
            record = False
            description = ''
            for type, value, line in XMLParser(data):
                if type == START_ELEMENT:
                    tag_uri, tag_name, attributes = value
                    record = True if tag_name == 'description' else False
                elif type == TEXT and record:
                    description = value
                elif type == END_ELEMENT:
                    record = False

            # Update value
            setup = db.get_handler(f.uri, cls=ConfigFile)
            setup.set_value("description", strong_escape(description))

            # Print and update status
            print "[%d] %s updated" % (count, '/'.join(splited[i:]))
            count += 1

        # Save database changes
    db.database.save_changes()
    errors.close()

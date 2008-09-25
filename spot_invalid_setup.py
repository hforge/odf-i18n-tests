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
""" spot any malformed setup.conf file"""


# Import from itools
from itools.vfs import traverse
from itools.handlers import Database, ConfigFile, get_handler

if __name__ == '__main__':
    db = Database().get_handler('documents')
    for f in db.traverse():
        if str(f.uri).endswith('setup.conf'):
            try:
                ConfigFile(f.uri).has_value('dummy')
            except SyntaxError, e:
                print "%s is not well formed:" % f.uri
                print str(e)

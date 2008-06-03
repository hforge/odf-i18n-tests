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


# Import from itools
from itools.vfs import vfs
from itools.handlers import get_handler
from itools.odf import ODTFile, ODPFile, ODSFile


def get_unitests_handlers():
    """Return list of tuple
      [(odf_handler1, po_handler1),
       (odf_handler2, po_handler)]
    """
    handlers = []
    # We traverse all ODF documents
    for handler in vfs.traverse('./documents/'):
        handler = get_handler(handler.path)
        is_odf_document = isinstance(handler, (ODTFile, ODPFile, ODSFile))
        if not is_odf_document:
            continue
        # We found a ODF Document, We search the corresponding PO file
        po_uri = handler.uri.resolve('%s.po' % 'testDoc')
        po_handler = get_handler(po_uri)
        handlers.append((handler, po_handler))
    return handlers

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
from itools.handlers import get_handler
from itools.gettext.po import encode_source
import itools.odf

# Import from odf i18n tests
from utils import start_test


def itools_handler(filename):
    handler = get_handler(filename)
    return [encode_source(unit)
            for unit, context, reference in handler.get_units()]

if __name__ == '__main__':
    start_test(itools_handler)


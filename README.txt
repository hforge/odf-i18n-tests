=============================
====== ODF i18n tests =======
=============================

General description
---------------------

The test suite allow to check and validate the performance of itools.odf package
that allow to extract translatable messages from an ODF document. For more
informations see the website:

    http://www.ikaaro.org/odf/;view

For momment, the units tests used a set of sample documents for the OpenDocument
specification:

    http://develop.opendocumentfellowship.com/testsuite/testcases/


License
----------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.



Install & Test
-----------------------

You have to install itools (dvp version - master branch):

    $ git-clone http://lleu.org/itools.git
    $ python setup.py install

To launch unitests you just have to type:

    $ python test_itools.py


Copyright
-------------

  - Romain Gauthier <romain@itaapy.com>
  - Juan David Ibáñez Palomar <jdavid@itaapy.com>
  - Sylvain Taverne <sylvain@itaapy.com>

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

The odf-i18n-test testsuite and all data and files related are licensed under the
Creative Commons Attribution 3.0 licence. In short, this means you can freely
reuse and distribute this content, also commercially, for as long you provide a
proper attribution.
for more details, see:

    http://creativecommons.org/licenses/by/3.0/

The odf-i18n-test testsuite, and especially the ODF documents, are based on
another testsuite, available here:

    http://develop.opendocumentfellowship.com/testsuite/

This testsuite is also licensed under the Creative Commons Attribution license
in the 2.5 version.
for more details, see:

    http://develop.opendocumentfellowship.com/testsuite/LICENSE.html
    http://creativecommons.org/licenses/by/2.5/


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

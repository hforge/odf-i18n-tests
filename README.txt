
The purpose of this test suite is to check the correctness of tools that
extract text from an ODF document for translation.  Currently there are
two scripts to test two toolsets; this is the procedure for testing:

1. Install itools & the translate toolkit, download from:

   http://www.hforge.org/itools
   http://translate.sourceforge.net/wiki/toolkit/index

2. Run the tests:

  $ python test_itools.py
  $ python test_ttk.py

There are 226 test cases, the input for each test is an ODF document and
the output is a PO file.

The test suite is available online for browsing:

  http://www.hforge.org/odf-i18n-tests


Credits
=======

This test suite is derived from the ODF test suite of the OpenDocument
Fellowship:

  http://develop.opendocumentfellowship.com/testsuite/

We reproduce here the authorship of the original work:

 "The set of sample documents was developed at the Networking and Mobile
  Computing Laboratory at the School of Electrical Engineering and Computer
  Science of the University of Central Florida.

  Developed by: Yi Luo and Majid A. Khan under the supervision of Lotzi
  Bölöni."

This derivative work was a deliverable of the OpenDocument Translation
Converter" [1] project sponsored by the NLnet foundation [2], developed
by the project partner Itaapy [3] and assisted by the project partner
translate.org.za [4].

Working at Itaapy, Romain Gauthier did most of the work, he selected the
relevant test cases from the original test suite and added by hand the
expected PO files.  Other people involved include J. David Ibáñez, David
Versmisse, Gautier Hayoun and Sylvain Taverne.

[1] http://translate.sourceforge.net/wiki/developers/projects/odf
[2] http://www.nlnet.nl/
[3] http://www.itaapy.com/
[4] http://translate.org.za/


License
=======

This test suite is available under the terms and conditions of the Creative
Commons Attribution 3.0 Unported license.  See the LICENSE.txt file for
further details, or check the license online:

  http://creativecommons.org/licenses/by/3.0/
  http://creativecommons.org/licenses/by/3.0/legalcode


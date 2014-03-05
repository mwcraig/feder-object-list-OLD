Objects observed at Feder Observatory
=====================================

[![Build Status](https://travis-ci.org/mwcraig/feder-object-list.png?branch=master)](https://travis-ci.org/mwcraig/feder-object-list)

The file ``feder_object_list.csv`` in this repository contains the object name,
RA and Dec of objects observed at the Feder Observatory. It is used to add
object names to images during header processing.

View/edit the list of objects
=============================

Click on the file name in the list above. If you want to edit the object list to
add an object, click the "Edit" button above the list of objects.

Use this object list in header processing
=========================================

The scripts/functions for adding object names in header processing have a way of
specifying the name of the object list. Use this name to use the latest version
of the list here:
``https://raw.github.com/mwcraig/feder-object-list/master/feder_object_list.csv``

For maintainers of this list
============================

Please do not merge pull requests until the Travis build reports the pull
request passes. The check on Travis will:

+ Make sure the object file is readable as an Astropy table. Attempt to verify
+ the RA/Dec specified for the object by looking up the object position in
  Simbad.

If the travis build fails click on the fail message in the pull request, which
will take you to the log of the travis build. Then:

+ If the error is a timeout try re-running the build (simbad may be down).
+ If the log reports that the position given for the object doesn't match the
  simbad position, verify the position in simbad.
+ If the position is really incorrect ask the person who made the pull request
  to fix it.

Limitations of this automated checking
--------------------------------------

If the name isn't recognized by simbad the checker skips over it. There are some
objects (e.g. MU Vul) that simbad should recognize, but doesn't, and others
(e.g. sa104) that are standard star fields not list as names in simbad.

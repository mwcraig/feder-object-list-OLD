from __future__ import print_function, division

from exceptions import Exception

from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy.coordinates.name_resolve import NameResolveError
from astropy import units as u
from astropy import utils


class CoordinateMismatchError(Exception):
    pass

TABLE_NAME = 'feder_object_list.csv'
MAX_SEP = 30  # arcsec

# increase timeout so that the Travis builds succeed
utils.data.conf.remote_timeout = 30

# Failures that are allowed to occur because they have been hand verified.
# Add the name of the object as the key and the expected error as the value.
# Also add a reference for the coordinates or a brief explanation.
ALLOWED_FAILURES = {
    'nsv 4863': NameResolveError, # in VSX https://www.aavso.org/vsx/index.php?view=detail.top&revid=208743
    'sa111': NameResolveError, # Found in simbad, but no coordinates
    'sa104': CoordinateMismatchError, # Field is wide, our center differs by several arcmin
    'sa110': CoordinateMismatchError, # Same as SA104...
}


def test_table_can_be_read_and_coords_good():
    objs = Table.read(TABLE_NAME)
    columns = ['object', 'ra', 'dec']
    for col in columns:
        assert col in objs.colnames

    failures = {}
    for row in objs:
        object_name = row['object']
        try:
            simbad_pos = SkyCoord.from_name(object_name)
        except NameResolveError:
            failures[object_name] = NameResolveError
            continue

        table_pos = SkyCoord(row['ra'], row['dec'], unit=(u.hour, u.degree))
        # CHANGE ASSERT TO IF/THEN, print name then assert 0
        sep = table_pos.separation(simbad_pos).arcsec
        warn = ''
        if sep > MAX_SEP:
            warn = ('Bad RA/Dec for object {}, '
                    'separation is {} arcsec'.format(object_name, sep))
            if object_name not in ALLOWED_FAILURES.keys():
                print(warn)
            failures[object_name] = CoordinateMismatchError

    real_failures = {}
    for name, fail in failures.iteritems():
        try:
            assert ALLOWED_FAILURES[name] == fail
        except (KeyError, AssertionError):
            # Either way, this was an unexpected failure.
            real_failures[name] = fail

    if real_failures:
        print(real_failures)

    assert len(real_failures) == 0

from astropy.table import Table
from astropy.coordinates import ICRS, name_resolve
from astropy import units as u

TABLE_NAME = 'feder_object_list.csv'
MAX_SEP = 5  # arcsec

# increase timeout so that the Travis builds succeed
name_resolve.NAME_RESOLVE_TIMEOUT.set(30)


def test_table_can_be_read_and_coords_good():
    objs = Table.read(TABLE_NAME, format='ascii', delimiter=',')
    columns = ['object', 'ra', 'dec']
    for col in columns:
        assert col in objs.colnames
    for row in objs:
        try:
            simbad_pos = ICRS.from_name(row['object'])
        except name_resolve.NameResolveError:
            continue
        table_pos = ICRS(row['ra'], row['dec'], unit=(u.hour, u.degree))
        # CHANGE ASSERT TO IF/THEN, print name then assert 0
        sep = table_pos.separation(simbad_pos).arcsec
        warn = ''
        if sep > MAX_SEP:
            warn = ('Bad RA/Dec for object {}, '
                    'separation is {} arcsec'.format(row['object'], sep))
            print (warn)
        assert len(warn) == 0

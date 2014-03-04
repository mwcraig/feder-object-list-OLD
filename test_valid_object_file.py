from astropy.table import Table

TABLE_NAME = 'feder_object_list.csv'


def test_table_can_be_read():
    objs = Table.read(TABLE_NAME, format='ascii', delimiter=',')
    columns = ['object', 'ra', 'dec']
    for col in columns:
        assert col in objs.colnames

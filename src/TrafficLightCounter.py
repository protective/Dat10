import pg , math, sys, os ,time

USER = 'd103'
DB = "gps_can"
PREFIX = 'a'
if len(sys.argv) > 1:
	PREFIX = sys.argv[1]
QUERY_TABLE = ""+PREFIX+"_gps_can_data"
TABLE = ""+PREFIX+"_trip_data"


con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')



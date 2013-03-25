import os, pg, math, sys, time
#1 = idle
USER = 'd103'
DB = 'gps_can'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

test= False
PREFIX = 'a'
if len(sys.argv) > 1:
	PREFIX = sys.argv[1]
DATATABLE = ""+PREFIX+"_gps_can_data"
TRIPDATA = ""+PREFIX+"_trip_data"

"""
print "Altering table"
con.query('alter table ' + DATATABLE + ' drop IF EXISTS idleRange;')
con.query('alter table ' + DATATABLE + ' add column idleRange int not null default 0;')

con.query('update ' + DATATABLE + ' set idleRange = 1 where rpm>0 and speed = 0;')

print "Creating index"
con.query("DROP INDEX IF EXISTS idle_" + DATATABLE + "_idx;")
con.query("Create index idle_" + DATATABLE + "_idx on " + DATATABLE + " (idleRange);")
"""

res = con.query("select timestamp from " + DATATABLE + " where idleRange=1 order by timestamp;").getresult()
for r in res:
	print r[0]



if test:
	print "Counting idle"
	output = open('data/idleDuration.csv', 'a')
	temp = con.query("select count(*) from " + DATATABLE + " where idle=1;").getresult()[0][0];
	print >> output, str(duration) + " " + str(temp)
	print str(duration) + " " + str(temp)

import random, time, math, pg, sys

DB = sys.argv[1]
TABLE = sys.argv[2]
NEW_TABLE = 'a_' + TABLE

con = pg.connect(dbname=DB, host='localhost', user='sabrine',passwd='F1ff')

if (False):
	print "Alter table"
	con.query('create table ' + NEW_TABLE + ' as (select * from ' + TABLE + ');')
	con.query('alter table ' + NEW_TABLE + ' add column tid int;')
if (False):
	print "Creating indexes"
	con.query("DROP INDEX IF EXISTS vehid_" + NEW_TABLE + "_idx CASCADE; create index vehid_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (vehicleid);")
	con.query("DROP INDEX IF EXISTS time_" + NEW_TABLE + "_idx CASCADE; create index time_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (timestamp);")
	con.query("DROP INDEX IF EXISTS tid_" + NEW_TABLE + "_idx CASCADE; create index tid_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (tid);")

print "Fetching data"
res = con.query('select vehicleid, timestamp from ' + NEW_TABLE + ' where vehicleid=354330030781010 order by vehicleid, timestamp').getresult()

tid=0
prevTime = time.mktime(time.strptime("2000-01-01 00:00:00", "%Y-%m-%j %H:%M:%S"))

print "Processing data"
for p in res:
	curTime = time.mktime(time.strptime(p[1], "%Y-%m-%j %H:%M:%S"))
	
	if abs(prevTime - curTime) > 100:
		tid+=1
	prevTime = curTime
	
	con.query('update ' + NEW_TABLE + ' set tid=' + str(tid) + " where timestamp='" + str(p[1]) + "' and vehicleid=" + str(p[0]) + ";");
	#print str(tid) + "\t" + p[1]



import random, time, math, pg, sys

DB = sys.argv[1]
TABLE = sys.argv[2]
NEW_TABLE = 'a_' + TABLE

print "Connecting to " + DB
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
res = con.query('select vehicleid, timestamp from ' + NEW_TABLE + ' where tid is null or tid=10202 order by vehicleid, timestamp').getresult()

tid=10202
prevtid = tid
startTime = res[0][1]
prevTime = time.mktime(time.strptime(startTime, "%Y-%m-%j %H:%M:%S"))
prevVhId = res[0][0]
counter = 0


print "Processing data"
for p in range(0,len(res)):		
	curTime = time.mktime(time.strptime(res[p][1], "%Y-%m-%j %H:%M:%S"))
	curVhId = res[p][0]

	if abs(prevTime- curTime) > 100 or not prevVhId == curVhId or p==len(res):
		con.query('update ' + NEW_TABLE + ' set tid=' + str(tid) + " where timestamp>='" + startTime + "' and timestamp<='" + res[p-1][1] + "' and vehicleid=" + str(curVhId) + ";")
		
		startTime = res[p][1]
		tid += 1
	
	prevTime = curTime
	prevVhId = curVhId
		
	if p%1000 == 0:
		print "Processed entry " + str(p)


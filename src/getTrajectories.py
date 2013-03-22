import random, time, math, pg, sys,os

USER = 'd103'
DB = 'gps_can'
TABLE = 'gps_can_data'
NEW_TABLE = 'b_' + TABLE

TIME = 120
LENGTH = 30
test = False
filename = ''
if len(sys.argv) > 1:
	TIME = int(sys.argv[1])
	LENGTH = int(sys.argv[2])
	if len(sys.argv)> 3:
		test = bool(sys.argv[3])
		filename = str(sys.argv[4])
		
counter = 0
	

print str(TIME) + " seconds timeframe and " + str(LENGTH) + " length."

print "Connecting to " + DB
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

if (not test):
	print "Alter table"
	con.query('drop table IF EXISTS ' + NEW_TABLE + ';')
	con.query('create table ' + NEW_TABLE + ' as (select * from ' + TABLE + ' where rpm > 0);')
	con.query('alter table ' + NEW_TABLE + ' add column tid int;')
	con.query('alter table ' + NEW_TABLE + ' add column dirty bool default false;')
if (not test):
	print "Creating indexes"
	con.query("DROP INDEX IF EXISTS vehid_" + NEW_TABLE + "_idx CASCADE; create index vehid_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (vehicleid);")
	con.query("DROP INDEX IF EXISTS time_" + NEW_TABLE + "_idx CASCADE; create index time_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (timestamp);")
	con.query("DROP INDEX IF EXISTS speed_" + NEW_TABLE + "_idx CASCADE; create index speed_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (speed);")
	con.query("DROP INDEX IF EXISTS rpm_" + NEW_TABLE + "_idx CASCADE; create index rpm_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (rpm);")
	

print "Fetching data"
res = con.query('select vehicleid, timestamp from ' + TABLE + ' where rpm > 0 order by vehicleid, timestamp').getresult()

tid=0
startTime = res[0][1]
prevTime = time.mktime(time.strptime(startTime, "%Y-%m-%j %H:%M:%S"))
prevVhId = res[0][0]


print "Processing data"
for p in range(0,len(res)):		
	curTime = time.mktime(time.strptime(res[p][1], "%Y-%m-%j %H:%M:%S"))
	curVhId = res[p][0]
	diff = abs(prevTime - curTime)
	

	if diff > TIME or prevVhId != curVhId:
		length = abs(time.mktime(time.strptime(startTime, "%Y-%m-%j %H:%M:%S")) - time.mktime(time.strptime(res[p-1][1], "%Y-%m-%j %H:%M:%S")))
		if length >= LENGTH:
			query = 'update ' + NEW_TABLE + ' set tid=' + str(tid)
			counter +=1
		else:
			query = 'update ' + NEW_TABLE + ' set tid='+ str(tid) + ', dirty=true '
	
		query += " where timestamp>='" + startTime + "' and timestamp<='" + res[p-1][1] + "' and vehicleid=" + str(res[p-1][0]) + ";"

		if( not test):
			con.query(query)
			
		startTime = res[p][1]
		tid += 1
	
	prevTime = curTime
	prevVhId = curVhId
		
	if p%5000 == 0:
		print "Processed entry " + str(p)

length = abs(time.mktime(time.strptime(startTime, "%Y-%m-%j %H:%M:%S")) - time.mktime(time.strptime(res[p-1][1], "%Y-%m-%j %H:%M:%S")))
print length
if length >= LENGTH:
	query = 'update ' + NEW_TABLE + ' set tid=' + str(tid)
	counter +=1
else:
	query = 'update ' + NEW_TABLE + ' set tid='+ str(tid) + ', dirty=true '

query += " where timestamp>='" + startTime + "' and timestamp<='" + res[len(res)-1][1] + "' and vehicleid=" + str(res[len(res)-1][0]) + ";"
if( not test):
	con.query(query)

if not test:
	print "Creating index"
	con.query("DROP INDEX IF EXISTS tid_" + NEW_TABLE + "_idx CASCADE; create index tid_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (tid);")

if(test):
	output = open('data/'+filename, 'a')
	s = str(TIME) + " " + str(LENGTH) + " " + str(counter)
	print s 
	print >> output, s

print "Done"


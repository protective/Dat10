import random, time, math, pg, sys,os

USER = os.getlogin()
DB = 'gps_can'
TABLE = 'gps_can_data'
NEW_TABLE = 'a_' + TABLE
if len(sys.argv) > 1:
	TIME = int(sys.argv[1])
	OBS = int(sys.argv[2]) #Number of observations per minut
else:
	TIME = 120
	OBS = 2


print "Testing with " + str(TIME) + " seconds."

print "Connecting to " + DB
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

if (True):
	print "Alter table"
	con.query('drop table IF EXISTS ' + NEW_TABLE + ';')
	con.query('create table ' + NEW_TABLE + ' as (select * from ' + TABLE + ' where vehicleid=354330030804267;')
	con.query('alter table ' + NEW_TABLE + ' add column tid int;')
	con.query('alter table ' + NEW_TABLE + ' add column dirty bool default false;')
if (True):
	print "Creating indexes"
	con.query("DROP INDEX IF EXISTS vehid_" + NEW_TABLE + "_idx CASCADE; create index vehid_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (vehicleid);")
	con.query("DROP INDEX IF EXISTS time_" + NEW_TABLE + "_idx CASCADE; create index time_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (timestamp);")
	#con.query("DROP INDEX IF EXISTS speed_" + NEW_TABLE + "_idx CASCADE; create index speed_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (speed);")
	#con.query("DROP INDEX IF EXISTS rpm_" + NEW_TABLE + "_idx CASCADE; create index rpm_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (rpm);")
	#con.query("DROP INDEX IF EXISTS totalconsumed_" + NEW_TABLE + "_idx CASCADE; create index totalconsumed_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (totalconsumed);")
	#con.query("DROP INDEX IF EXISTS kmcounter_" + NEW_TABLE + "_idx CASCADE; create index kmcounter_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (kmcounter);")
	

print "Fetching data"
res = con.query('select vehicleid, timestamp from ' + TABLE + ' where rpm > 0 order by vehicleid, timestamp').getresult()

tid=0
startTime = res[0][1]
prevTime = time.mktime(time.strptime(startTime, "%Y-%m-%j %H:%M:%S"))
prevVhId = res[0][0]
counter = 0


print "Processing data"
for p in range(0,len(res)):		
	curTime = time.mktime(time.strptime(res[p][1], "%Y-%m-%j %H:%M:%S"))
	curVhId = res[p][0]
	diff = abs(prevTime - curTime)
	counter +=1

	if diff > TIME or prevVhId != curVhId:
		length = time.mktime(time.strptime(startTime, "%Y-%m-%j %H:%M:%S")) - time.mktime(time.strptime(res[p-1][1], "%Y-%m-%j %H:%M:%S"))
		if length/float(counter) > OBS:
			query = 'update ' + NEW_TABLE + ' set tid=' + str(tid)
		else:
			query = 'update ' + NEW_TABLE + ' set tid='+ str(tid) + ', dirty=true '
		
		query += " where timestamp>='" + startTime + "' and timestamp<='" + res[p-1][1] + "' and vehicleid=" + str(res[p-1][0]) + ";"
		con.query(query)
		startTime = res[p][1]
		counter=0
		tid += 1
	
	prevTime = curTime
	prevVhId = curVhId
		
	if p%5000 == 0:
		print "Processed entry " + str(p)

length = time.mktime(time.strptime(startTime, "%Y-%m-%j %H:%M:%S")) - time.mktime(time.strptime(res[len(res)-1][1], "%Y-%m-%j %H:%M:%S"))
if length/float(counter) > OBS:
	query = 'update ' + NEW_TABLE + ' set tid=' + str(tid)
else:
	query = 'update ' + NEW_TABLE + ' set tid='+ str(tid) + ', dirty=true '

query += " where timestamp>='" + startTime + "' and timestamp<='" + res[len(res)-1][1] + "' and vehicleid=" + str(res[len(res)-1][0]) + ";"
con.query(query)

print "Creating index"
con.query("DROP INDEX IF EXISTS tid_" + NEW_TABLE + "_idx CASCADE; create index tid_" + NEW_TABLE + "_idx on " + NEW_TABLE + " (tid);")

#print "Counting trips"
#output = open('numberOfTrajectories.csv', 'a')
#print >> output, str(TIME) + "\t" + str(con.query("select count(distinct tid) from " + NEW_TABLE).getresult()[0][0])

print "Done"


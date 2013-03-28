import os, pg, math, sys, time
#1 = idle
USER = 'd103'
DB = 'gps_can'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

test= False
try:
	DATATABLE = sys.argv[1] + "_gps_can_data"
	NEWTABLE = sys.argv[1] + "_vehicledata"
except:
	print 'Error: remember the parameters'
	exit(1)

if False:
	print "Altering table"
	con.query('alter table ' + DATATABLE + ' drop IF EXISTS idleRange;')
	con.query('alter table ' + DATATABLE + ' add column idleRange int not null default 0;')

	con.query('update ' + DATATABLE + ' set idleRange = 1 where rpm>0 and speed = 0;')

	print "Creating index"
	con.query("DROP INDEXDATATABLE IF EXISTS idle_" + DATATABLE + "_idx;")
	con.query("Create index idle_" + DATATABLE + "_idx on " + DATATABLE + " (idleRange);")


con.query("drop table if exists "+NEWTABLE+";")
con.query("create table "+NEWTABLE+" (vehicleid bigint, idleRange int, fuel float, starTime timestamp);")
print "Calculating"
vehicles = con.query("select distinct vehicleid from "+ DATATABLE + ";").getresult()

for v in vehicles:
	res = con.query("select timestamp, idleRange, totalconsumed, tid from " + DATATABLE + " where vehicleid=" + str(v[0]) +" and dirty is false order by timestamp;").getresult()
	s = -1
	fuel = 0
	for r in range(0, len(res)-1):		
		if (res[r][1] == 0 or ((r==len(res)-1 or not res[r-1][3]== res[r][3]) and res[r][1] == 1)) and not s==-1 and r > 0:
			t = time.mktime(time.strptime(res[r-1][0], "%Y-%m-%j %H:%M:%S"))
			if abs(t-s)> 0:
				fuel2 = res[r-1][2]
				con.query("insert into "+NEWTABLE+" values (" + str(v[0]) + ", " + str(abs(t-s)) + "," + str(abs(fuel2-fuel)) + ",'" + str(startTime) + "')")
			s = -1
			fuel = 0
		if res[r][1] == 1 and s== -1:
			s = time.mktime(time.strptime(res[r][0], "%Y-%m-%j %H:%M:%S"))
			startTime = res[r][0]
			fuel = res[r][2]

if test:
	print "Counting idle"
	output = open('data/idleDuration.csv', 'a')
	temp = con.query("select count(*) from " + DATATABLE + " where idle=1;").getresult()[0][0];
	print >> output, str(duration) + " " + str(temp)
	print str(duration) + " " + str(temp)

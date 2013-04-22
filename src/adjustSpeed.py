import os, pg, math, sys, time
#1 = idle
USER = 'd103'
DB = 'gps_can'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

test= False

try:
	DATATABLE = sys.argv[1] + "_gps_can_data"
except:
	print 'Error: remember the parameters'
	exit(1)


con.query('alter table ' + DATATABLE + ' drop IF EXISTS speedOld;')
con.query('alter table ' + DATATABLE + ' add column speedOld integer not null default 0;')
con.query('update ' + DATATABLE + ' set speedOld= s from (select speed as s from ' + DATATABLE + ')a;')

counter = 0
trips = con.query('select distinct tid from ' + DATATABLE +' where tid is not null').getresult()
for t in trips:
	trip = t[0]
	res = con.query("select timestamp, speed, acceleration2 from " + DATATABLE + " where tid=" + str(trip) + " and dirty is false order by timestamp;").getresult()
	for r in range (1, len(res)-2):
		acceleration = res[r][2]
		if acceleration > 3 or acceleration < 10:
			print res[r]
			s1 = float(res[r-1][1])
			s3 = float(res[r+1][1])
			t1 = float(time.mktime(time.strptime(res[r-1][0], "%Y-%m-%j %H:%M:%S")))
			t2 = float(time.mktime(time.strptime(res[r][0], "%Y-%m-%j %H:%M:%S")))
			t3 = float(time.mktime(time.strptime(res[r+1][0], "%Y-%m-%j %H:%M:%S")))
			newSpeed = s1 + (((s3-s1)/(t3-t1))*(t2-t1))
			q = "update " + DATATABLE + " set speed = " + str(newSpeed) + " where timestamp = " + res[r][0] + " and tid=" + str(trip) + ";"
			print q
			
			
			
			
			

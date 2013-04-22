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

def getTime(t):
	return float(time.mktime(time.strptime(t, "%Y-%m-%j %H:%M:%S")))


con.query('alter table ' + DATATABLE + ' drop IF EXISTS speedMod;')
con.query('alter table ' + DATATABLE + ' add column speedMod integer not null default 0;')
con.query('update ' + DATATABLE + ' set speedMod= speed;')

counter = 0
trips = con.query('select distinct tid from ' + DATATABLE +' where tid is not null').getresult()
for t in trips:
	trip = t[0]
	res = con.query("select timestamp, speed from " + DATATABLE + " where tid=" + str(trip) + " and dirty is false order by timestamp;").getresult()
	for r in range (1, len(res)-2):
		acc = 0
		if r > 0:
			acc = ((res[r][1]-res[r-1][1])/(getTime(res[r][0])-getTime(res[r-1][0]))/3.6)
		#print acc
		if acc > 3 or acc < -10:
			#print res[r]
			s1 = float(res[r-1][1])
			s3 = float(res[r+1][1])
			t1 = float(time.mktime(time.strptime(res[r-1][0], "%Y-%m-%j %H:%M:%S")))
			t2 = float(time.mktime(time.strptime(res[r][0], "%Y-%m-%j %H:%M:%S")))
			t3 = float(time.mktime(time.strptime(res[r+1][0], "%Y-%m-%j %H:%M:%S")))
			newSpeed = s1 + (((s3-s1)/(t3-t1))*(t2-t1))
			q = "update " + DATATABLE + " set speedMod = " + str(newSpeed) + " where timestamp = '" + res[r][0] + "' and tid=" + str(trip) + ";"
			print q
			con.query(q)
			
			
			
			
			

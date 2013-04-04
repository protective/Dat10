import os, pg, math, sys, time
USER = 'd103'
DB = 'gps_can'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

test= False
try:
	DATATABLE = sys.argv[1]
except:
	print 'Error: remember the parameters'
	exit(1)
	
def getTime(t):
	return float(time.mktime(time.strptime(t, "%Y-%m-%j %H:%M:%S")))

if True:
	print "Altering table"
	con.query('alter table ' + DATATABLE + ' drop IF EXISTS acceleration2;')
	con.query('alter table ' + DATATABLE + ' add column acceleration2 float not null default 0;')

	print "Calculating acceleration profiles"
	vehicles = con.query("select distinct vehicleid from "+ DATATABLE + ";").getresult()

	for v in vehicles:
		print "Vehicle " + str(v[0])
		res = con.query("select timestamp, speed, tid from " + DATATABLE + " where vehicleid=" + str(v[0]) +" and dirty is false order by timestamp;").getresult()
		oldTime = res[0][0]
		oldSpeed = float(res[0][1])
		oldTid = int(res[0][2])
		for r in range(1, len(res)-1):
			curTime = res[r][0]
			curSpeed = float(res[r][1])
			curTid = int(res[r][2])
			
			acc = 0
			if curTid == oldTid:
				acc = (oldSpeed-curSpeed)/(getTime(oldTime)-getTime(curTime))
			
			q = "update " + DATATABLE + " set acceleration2 = " + str(acc) + " where vehicleid=" + str(v[0]) + " and timestamp='"+ str(curTime) + "';"
			con.query(q)
			#print str(curTid)  + "\t" + str(acc) + "\t" + str(curTime) + "\t" + str(curSpeed) + "\t" + str(abs(oldSpeed-curSpeed)) + "\t" + str(abs(getTime(oldTime)-getTime(curTime)))
			
			oldTime = curTime
			oldSpeed = curSpeed
			oldTid = curTid
			

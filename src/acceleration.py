import os, pg, math, sys, time
USER = 'd103'
DB = 'gps_can'



con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

test= False
try:
	DATATABLE = sys.argv[1] + "_gps_can_data"
	ACCDATA = sys.argv[1] + "_accdata2"
except:
	print 'Error: remember the parameters'
	exit(1)
	
def getTime(t):
	return float(time.mktime(time.strptime(t, "%Y-%m-%j %H:%M:%S")))

if True:
	interval = 3
	print "Altering table"
	con.query('set synchronous_commit = on;')
	con.query('alter table ' + DATATABLE + ' drop IF EXISTS acceleration' + str(interval) + ';')
	con.query('alter table ' + DATATABLE + ' add column acceleration' + str(interval) + ' float not null default 0;')

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
		
			q = "update " + DATATABLE + " set acceleration" + str(interval) + " = " + str(acc) + " where vehicleid=" + str(v[0]) + " and timestamp='"+ str(curTime) + "';"
			con.query(q)
			#print str(curTid)  + "\t" + str(acc) + "\t" + str(curTime) + "\t" + str(curSpeed) + "\t" + str(abs(oldSpeed-curSpeed)) + "\t" + str(abs(getTime(oldTime)-getTime(curTime)))
		
			oldTime = curTime
			oldSpeed = curSpeed
			oldTid = curTid

	con.query("DROP INDEX IF EXISTS acceleration" + str(interval) + "_" + DATATABLE + "_idx CASCADE; create index acceleration" + str(interval) + "_" + DATATABLE + "_idx on " + DATATABLE + " (acceleration" + str(interval) + ");")

if False:
	con.query("drop table if exists "+ACCDATA+";")
	con.query("create table "+ACCDATA+" (vehicleid bigint, acceleration float, fuel float, int time, startTime timestamp);")

	print "Calculating"
	vehicles = con.query("select distinct vehicleid from "+ DATATABLE + ";").getresult()
	for v in vehicles:
		print "Vehicle " + str(v[0])
		res = con.query("select tid, timestamp, acceleration2, totalconsumed from " + DATATABLE + " where vehicleid=" + str(v[0]) +" and dirty is false order by timestamp;").getresult()
		oldTid = res[0][0]
		oldTime = res[0][1]
		oldAcc = float(res[0][2])
		oldFuel = float(res[0][3])
		
		startTime = oldTime
		startFuel = oldFuel
		
		totalAcc= oldAcc
		
		for r in range(0, len(res)-1):
			tid = res[r][0]
			ctime = res[r][1]
			acc = float(res[r][2])
			fuel = float(res[r][3])
						
			accSign = 0 
			if acc< 0:
				accSign =-1
			if acc>0:
				accSign = 1
			
			oldAccSign = 0 
			if oldAcc< 0:
				oldAccSign =-1
			if oldAcc>0:
				oldAccSign = 1
			 
			if (not accSign == oldAccSign) or (not oldTid == tid):
				timeDiff= abs(getTime(startTime)-getTime(oldTime))
				if timeDiff>0:
					con.query("insert into " + ACCDATA + " values (" + str(v[0]) +", " + str(totalAcc/timeDiff) + ", " + str(abs(startFuel-oldFuel)) +"," + str(timeDiff) + ",'" + str(startTime) + "');")
					#print "\t" + str(startTime) + "\t" + str(oldTime) + "\t" +  str(abs(startFuel-oldFuel)) + "\t" + str(totalAcc) + "\t" + str(totalAcc/timeDiff)
				totalAcc =0
				startTime = ctime
				startFuel = fuel
			#print str(tid) + "\t" + str(ctime) + "\t" + str(acc) + "\t" + str(fuel)
			
			totalAcc += acc
			oldTid = tid
			oldAcc = acc
			oldTime = ctime
			oldFuel = fuel

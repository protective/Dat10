import os, pg, math, sys, time
USER = 'd103'
DB = 'gps_can'



con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

test= False

errormargin = 40
try:
	DATATABLE = sys.argv[1] + "_gps_can_data"
	ACCDATA = sys.argv[1] + "_accdata3"
except:
	print 'Error: remember the parameters'
	exit(1)
	
def getTime(t):
	return float(time.mktime(time.strptime(t, "%Y-%m-%j %H:%M:%S")))

if True:
	interval = 3
	print "Altering table"
	con.query('set synchronous_commit = on;')
	#con.query('alter table ' + DATATABLE + ' drop IF EXISTS acceleration3;')
	#con.query('alter table ' + DATATABLE + ' add column acceleration3 float default null;')

	con.query('alter table ' + DATATABLE + ' drop IF EXISTS acceleration2;')
	con.query('alter table ' + DATATABLE + ' add column acceleration2 float default null;')

	print "Calculating acceleration profiles"
	tids = con.query("select distinct tid from "+ DATATABLE + " order by tid;").getresult()
#	tids = []
#	for i in range(6002,6501):
#		tids.append([str(i)])

	for v in tids:
		print "tid " + str(v[0])
		res = con.query("select timestamp, speedMod, tid from " + DATATABLE + " where tid=" + str(v[0]) +" and dirty is false order by timestamp;").getresult()

		if len(res) > 0:
			oldTime = res[0][0]
			oldspeed = res[0][1]
			
			for r in range(0,len(res)-1):
				if str(res[r][1])=='None':
					continue
				curTime = res[r][0]
				acc = 0
				if(getTime(curTime)-getTime(oldTime) > 0):
					acc = ((res[r][1]-oldspeed)/float(getTime(curTime)-getTime(oldTime)))/3.6
				
				if(getTime(curTime)-getTime(oldTime) <= 2):
					#q = "update " + DATATABLE + " set acceleration3 = " + str(acc) + " where tid=" + str(res[2][2]) + " and timestamp='"+ str(res[r][0]) + "';"				
					q = "update " + DATATABLE + " set acceleration2 = " + str(acc) + " where tid=" + str(res[2][2]) + " and timestamp='"+ str(res[r][0]) + "';"		
					con.query(q)
				
				oldspeed = res[r][1]
				oldTime = res[r][0]

	con.query("DROP INDEX IF EXISTS acceleration2_" + DATATABLE + "_idx CASCADE; create index acceleration2_" + DATATABLE + "_idx on " + DATATABLE + " (acceleration2);")

if False:
	con.query("drop table if exists "+ACCDATA+";")
	con.query("create table "+ACCDATA+" (vehicleid bigint, tid int, startTime timestamp, endTime timestamp, time int, startSpeed int, endSpeed int, acceleration float, avgAcceleration float, fuel float, km float);")

	print "Calculating"
	vehicles = con.query("select distinct vehicleid from "+ DATATABLE + ";").getresult()
	for v in vehicles:
		print "Vehicle " + str(v[0])
		res = con.query("select tid, timestamp, acceleration3, totalconsumed, speedmod, kmcounter from " + DATATABLE + " where vehicleid=" + str(v[0]) +" and dirty is false order by timestamp;").getresult()
		startIndex = 0		
		
		counter = 0
		totalAcc = 0
		oldAccSign = 0
		dirty = False
		
		for r in range(0, len(res)):
			fuelTemp = 0
			if r> 0:
				fuelTemp = int(((res[r][3]-res[r-1][3])*1000)/(getTime(res[r][1])-getTime(res[r-1][1])))
			if str(res[r][2]) == 'None' or (fuelTemp<0 or fuelTemp>20):
				dirty = True
				continue
			
			acc = float(res[r][2])
					
			accSign = 0 
			if acc< 0:
				accSign =-1
			if acc>0:
				accSign = 1
		
			if (r> 0 and ((not accSign == oldAccSign) or (not res[r-1][0] == res[r][0]))) or r == len(res)-1:
				endIndex = r-1
				if r== len(res)-1:
					endIndex = r
					totalAcc += acc
					counter += 1
			
				timeDiff= abs(getTime(res[startIndex][1])-getTime(res[endIndex][1]))

				if timeDiff>0 and not dirty:
					curAcc = (int(res[endIndex][4]) - int(res[startIndex][4]))/timeDiff
					avgAcc = float(totalAcc)/counter
					fuel = abs(float(res[endIndex][3]) - float(res[startIndex][3]))
					km = abs(float(res[endIndex][5]) - float(res[startIndex][5]))
				
					q= "insert into " + str(ACCDATA) + " values (" + str(v[0]) + ", " +str(res[endIndex][0]) + ", '" + str(res[startIndex][1]) + "', '" + str(res[endIndex][1]) + "', " + str(timeDiff) + ", " + str(res[startIndex][4]) + ", " + str(res[endIndex][4]) + ", " + str(curAcc) + ", " + str(avgAcc) + ", " + str(fuel) + ", " + str(km) + ")"
					#print q
					con.query(q)
				totalAcc = 0
				counter = 0
				startIndex = r
				dirty = False
		
			oldAccSign = accSign
			counter += 1
			totalAcc += acc

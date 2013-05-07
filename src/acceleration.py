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

if False:
	interval = 3
	print "Altering table"
	con.query('set synchronous_commit = on;')
	con.query('alter table ' + DATATABLE + ' drop IF EXISTS acceleration3;')
	con.query('alter table ' + DATATABLE + ' add column acceleration3 float default null;')

	print "Calculating acceleration profiles"
	tids = con.query("select distinct tid from "+ DATATABLE + " order by tid;").getresult()

	avgnumber = 1	

	for v in tids:
		print "tid " + str(v[0])
		res = con.query("select timestamp, speedMod, tid from " + DATATABLE + " where tid=" + str(v[0]) +" and dirty is false order by timestamp;").getresult()

		avg = float(0)
		oldavg = float(0)
		if len(res) > 0:
			oldTime = res[0][0]
			
			for r in range(0,len(res)-1):
				avg = 0
				counter = 0
				for a in range( max((r-avgnumber)+1,0),r+1):
					avg+=res[a][1]
					counter+=1
				if(counter > 0):
					avg/=counter
					curTime = res[r][0]
					acc = 0
					if(getTime(curTime)-getTime(oldTime) > 0):
						acc = ((avg-oldavg)/float(getTime(curTime)-getTime(oldTime)))/3.6
					oldavg = avg
					oldTime = res[r][0]
					
					if(getTime(curTime)-getTime(oldTime) <= 2):
						q = "update " + DATATABLE + " set acceleration3 = " + str(acc) + " where tid=" + str(res[2][2]) + " and timestamp='"+ str(res[r][0]) + "';"				
					con.query(q)

	con.query("DROP INDEX IF EXISTS acceleration2_" + DATATABLE + "_idx CASCADE; create index acceleration2_" + DATATABLE + "_idx on " + DATATABLE + " (acceleration2);")

if True:
	con.query("drop table if exists "+ACCDATA+";")
	con.query("create table "+ACCDATA+" (vehicleid bigint, tid int, startTime timestamp, endTime timestamp, startSpeed int, endSpeed int, acceleration float, avgAcceleration float, fuel float, km float);")

	print "Calculating"
	vehicles = con.query("select distinct vehicleid from "+ DATATABLE + ";").getresult()
	for v in vehicles:
		print "Vehicle " + str(v[0])
		res = con.query("select tid, timestamp, acceleration3, totalconsumed, speedmod, kmcounter from " + DATATABLE + " where vehicleid=" + str(v[0]) +" and dirty is false and acceleration3 is not null order by timestamp;").getresult()
		startIndex = 0		
		
		counter = 0
		totalAcc = 0
		oldAccSign = 0
		
		for r in range(0, len(res)):
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

				if timeDiff>0:
					curAcc = (int(res[endIndex][4]) - int(res[startIndex][4]))/timeDiff
					avgAcc = float(totalAcc)/counter
					fuel = abs(float(res[endIndex][3]) - float(res[startIndex][3]))
					km = abs(float(res[endIndex][5]) - float(res[startIndex][5]))
					
					q= "insert into " + str(ACCDATA) + " values (" + str(v[0]) + ", " +str(res[endIndex][0]) + ", '" + str(res[startIndex][1]) + "', '" + str(res[endIndex][1]) + "', " + str(res[startIndex][4]) + ", " + str(res[endIndex][4]) + ", " + str(curAcc) + ", " + str(avgAcc) + ", " + str(fuel) + ", " + str(km) + ")"
					#print q
					con.query(q)
				totalAcc = 0
				counter = 0
				startIndex = r
			
			oldAccSign = accSign
			counter += 1
			totalAcc += acc

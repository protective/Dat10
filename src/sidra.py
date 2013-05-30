import pg, sys, os, csv, time

USER = 'd103'
DB = 'gps_can'
TABLE = 'trip_data'
if len(sys.argv) > 2:
	TABLE = sys.argv[2]
	
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

def getTime(t):
	return float(time.mktime(time.strptime(t, "%Y-%m-%j %H:%M:%S")))

def getEkp(tid, starttime, endtime, length):
	speeds = con.query("select speedmod, timestamp from g_gps_can_data where tid=" + str(tid) + " and timestamp>='" + str(starttime) + "' and timestamp<='" + str(endtime) + "' and speedmod is not null order by timestamp;").getresult()

	v = 0
	low = speeds[0][0]
	parsingAcc = True
	for s in range(1, len(speeds)):
		if speeds[s][0]>speeds[s-1][0]:
			parsingAcc = True
		if speeds[s][0]<speeds[s-1][0]:
			if parsingAcc:
				v+= speeds[s-1][0]**2-low**2
#				print str(low) + " " + str(speeds[s-1][0]) + " " + str(speeds[s-1][0]-low) + " " + str(speeds[s-1][1])
				parsingAcc= False
			low = speeds[s][0]
	return 0.00003858*v/length
	

def sidra(time, length, speed, ekp):
	ke1 = max(0.675-(1.22/speed), 0.5)
	ke2 =2.78+0.0178*speed

	ti = 0 #total idle time
	xs = length #total km
	ts = time #total time
	
	fi = 0.444*ti
	vr = (3600*xs)/float((ts-ti))
	fr = 1600/vr+30+0.0075*vr**2 + 108*ke1*ekp+54*ke2*ekp**2
	return (fi + fr*xs)/1000

#print getEkp(2239, '2012-10-23 14:24:31', '2012-10-23 14:26:27')

output = open('data/sidra.csv', 'w+')
trips = con.query("select time, length, fuel, cruisespeed, tid, starttime, endtime from g_cruise_data where length>0 order by cruisespeed;").getresult()
for t in trips:
	ekp = getEkp(t[4], t[5], t[6], t[1])
	s = sidra(t[0], t[1], t[3], ekp)
	if not str(s) == 'None':
		print >> output, str(t[3]) + " " + str(s) + " " + str(t[2]) + " " + str(t[2]-s) + " " + str(s/t[1]) + " " + str(t[2]/t[1])
output.close()
"""
output = open('data/sidraAcc.csv', 'w+')
trips = con.query("select time, km, fuel, endspeed, tid, starttime, endtime, avgAcceleration from g_accdata3 where km>0 and avgacceleration> 0 and time>=3 order by avgAcceleration;").getresult()
for t in trips:
	ekp = getEkp(t[4], t[5], t[6], t[1])
	s = sidra(t[0], t[1], t[3], ekp)
	if not str(s) == 'None':
		print >> output, str(t[7]) + " " + str(s) + " " + str(t[2]) + " " + str(t[2]-s) + " " + str(s/t[0]) + " " + str(t[2]/t[0])
output.close()
"""

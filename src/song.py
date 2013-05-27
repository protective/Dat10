import pg, sys, os, csv, time

USER = 'd103'
DB = 'gps_can'
TABLE = 'trip_data'
if len(sys.argv) > 2:
	TABLE = sys.argv[2]
	
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

def getTime(t):
	return float(time.mktime(time.strptime(t, "%Y-%m-%j %H:%M:%S")))


def song(tid, starttime, endtime):
	beta = 0.264
	gamma = 2.13
	epsilon = 18.3
	T = abs(getTime(endtime)- getTime(starttime))
	tau = 0
	speed = 0
	q = "select speedmod, acceleration3 from g_gps_can_data where tid=" + str(tid) + " and timestamp>='" + str(starttime) + "' and timestamp<='" + str(endtime) + "' and acceleration3 is not null order by timestamp"
	trip = con.query(q).getresult()
	if len(trip)>0:
		for t in trip:
			vt = float(t[0])/3.6 #Unit: m/s
			at = t[1]
			tau += max(vt*(1.1*at+0.132)+0.000302*vt**3, 0)
			speed += vt
			return ((beta*tau + T) / (gamma* (speed/epsilon)))/T
	return None


starts = con.query("select distinct round(startspeed/10)*10 as s from g_accdata3 order by s").getresult()
for s in starts:
	output = open('data/'+str(s[0])+'song.csv', 'w+')
	trips = con.query("select  tid, starttime, endtime, avgAcceleration, startspeed from g_accdata3 where round(startspeed/10)*10=" + str(s[0]) + " and avgAcceleration> 0 and time>10;").getresult()
	print s[0]
	for t in trips:
		s = song(t[0], t[1], t[2])
		if not str(s) == 'None':
			print >> output, str(t[3]) + " " + str(t[4]) + " " + str(s)
	output.close()

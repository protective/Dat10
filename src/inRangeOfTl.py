import pg , math, sys, os ,time

USER = "d103"
DB = "gps_can"


con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')


res = con.query("select max(tid) from a_gps_can_data").getresult()
print res

for i in range(0,res[0][0]):
	con.query("update a_gps_can_data set tl = (select tlId from trafficLights where ST_DISTANCE(trafficLights.geom,a_gps_can_data.geom) < 100 limit 1) where tid = "+ str(i) + ";")
	if i %10 == 0:
		print str(i) + " of " + str(res[0][0]) 





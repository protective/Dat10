import pg , math, sys, os ,time


USER = "d103"
DB = "gps_can"


con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')


res = con.query("select max(tid) from a_gps_can_data").getresult()
print res

for i in range(0,res[0][0]):
	con.query("update a_gps_can_data as a set tl = t.tlId from trafficlights as t where ST_Dwithin(t.geom,a.geom,100) and a.tid = "+ str(i) + ";")
	print str(i) + " of " + str(res[0][0]) 


#"update a_gps_can_data as a set tl = t.tlId from trafficlights as t where ST_Dwithin(t.geom,a.geom,100)"

#"explain update a_gps_can_data as a set tl = t.tlId from (select tlId from trafficlights where ST_Dwithin(geom,a.geom,100) )t"



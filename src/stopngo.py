#stop: below 10 km/t
#go: above 15 km/t

import pg, sys, os, csv

USER = 'd103'
DB = 'gps_can'
PREFIX = 'a'
if len(sys.argv) > 1:
	PREFIX = sys.argv[1]
QUERY_TABLE = ""+PREFIX+"_gps_can_data"
TABLE = ""+PREFIX+"_trip_data"


con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

con.query("alter table " + TABLE + " drop IF EXISTS stopngo;")
con.query('alter table ' + TABLE + ' add stopngo float not null default 0;')

print "Retreive data"
res = con.query("select tid, speedMod, timestamp, kmcounter from " + QUERY_TABLE + " where tid in (select tid from " + TABLE + ") and dirty is false order by tid, timestamp;").getresult()

print "Process data"
oldTid = res[0][0]
stoppedTime = ""
counter = 0
tempCounter = counter

for r in range(0, len(res)):
	tid = res[r][0]
	speed = res[r][1]
	time = res[r][2]

	if speed <= 10 and stoppedTime == "":
		stoppedTime = time
	
	if speed >= 15 and stoppedTime != "":
		counter += 1
		stoppedTime = ""
		
	
	if tid != oldTid:
		km = con.query("select total_km from " + TABLE + " where tid="+str(oldTid)+";").getresult()[0][0]
		stopngo = 0
		if km != 0:
			stopngo = counter/float(km)
		query = "update " + TABLE + " set stopngo = " + str(stopngo) + " where tid=" + str(oldTid) + ";"
		con.query(query)
	
		tempCounter = counter
		counter=0
		stoppedTime = ""
		

	oldTid = tid
	
	if r%100000 ==0:
		print "Processed entry " + str(r)
	
km = con.query("select total_km from " + TABLE + " where tid="+str(oldTid)+";").getresult()[0][0]
stopngo = 0
if km != 0:
	stopngo = tempCounter/float(km)
query = "update " + TABLE + " set stopngo = " + str(stopngo) + " where tid=" + str(oldTid) + ";"
con.query(query)









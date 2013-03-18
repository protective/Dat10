import os, pg, math, sys, time
#1 = idle
USER = 'd103'
con = pg.connect(dbname='gps_can', host='localhost', user=USER,passwd='F1ff')

duration = sys.argv[1]

print "Altering table"
con.query('alter table a_gps_can_data drop IF EXISTS idle;')
con.query('alter table a_gps_can_data add column idle int not null default 0;')

print 'Setting idle state with ' + str(duration) + " seconds duration"
#con.query("update a_gps_can_data set idle = 1 where speed = 0 and rpm > 0;")
trips = con.query('select distinct tid from trip_data').getresult()
for t in trips:
	trip = t[0]
	res = con.query("select timestamp, speed, rpm from a_gps_can_data where tid=" + str(trip) + " and dirty is false order by timestamp;").getresult() #
	start = ""
	for i in range(0,len(res)):
		ts = res[i][0]
		speed = res[i][1]
		rpm = res[i][2]

		if speed == 0 and rpm >0 and (start == "" or i==0):
			start = ts
		if start != "" and (speed > 0 or i==len(res)-1):
			end = res[i-1][0]
			if i==len(res)-1:
				end = res[i][0]
			
			sek = abs(time.mktime(time.strptime(start, "%Y-%m-%j %H:%M:%S")) - time.mktime(time.strptime(end, "%Y-%m-%j %H:%M:%S"))) + 1
			if sek > duration:
				con.query("update a_gps_can_data set idle 1 where tid="+ str(trip) + " and timestamp >=" +start + " and timestamp <=" + end +";")			
			start = ""

print "Creating index"
con.query("Create index idle_a_gps_can_data_idx on a_gps_can_data (idle);")


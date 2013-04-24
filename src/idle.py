import os, pg, math, sys, time
#1 = idle
USER = 'd103'
DB = 'gps_can'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')


try:
	DATATABLE = sys.argv[1] + "_gps_can_data"
	IDLEDATA = sys.argv[1] + "_idledatatl"
	TRIPDATA = sys.argv[1] + "_trip_data"
	duration = int(sys.argv[2])

except:
	print 'Error: remember the parameters'
	exit(1)


print "Finding stopped records"
con.query('alter table ' + DATATABLE + ' drop IF EXISTS stopped;')
con.query('alter table ' + DATATABLE + ' add column stopped int not null default 0;')

con.query('update ' + DATATABLE + ' set stopped = 1 where rpm>0 and speed = 0;')
con.query("DROP INDEX IF EXISTS stopped_" + DATATABLE + "_idx;")
con.query("Create index stopped_" + DATATABLE + "_idx on " + DATATABLE + " (stopped);")


print "Finding stopped periods"
con.query("drop table if exists "+IDLEDATA+";")
con.query("create table "+IDLEDATA+" (vehicleid bigint, stopped int, fuel float, startTime timestamp, endTime timestamp, length float, tid int);")

vehicles = con.query("select distinct vehicleid from "+ DATATABLE + ";").getresult()
for v in vehicles:
	print "Processing vehicle " + str(v[0])
	res = con.query("select timestamp, stopped, totalconsumed, tid, tl, kmcounter from " + DATATABLE + " where vehicleid=" + str(v[0]) +" and dirty is false order by timestamp;").getresult()
	s = -1
	fuel = 0
	length = 0
	stoppedAtTL = False 			
	for r in range(0, len(res)-1):
		if res[r][1]==1 and not res[r][4] == None:
			stoppedAtTL = True
#		print str(res[r][3]) + " " + str(res[r][0]) + " " + str(stoppedAtTL) + " " + str(type(res[r][4])) + " " + str(res[r][1])
		if (res[r][1] == 0 or ((r==len(res)-1 or not res[r-1][3]== res[r][3]) and res[r][1] == 1)) and not s==-1 and r > 0:
#			print "end"
			t = time.mktime(time.strptime(res[r-1][0], "%Y-%m-%j %H:%M:%S"))
			length2 = res[r-1][5]
			if abs(t-s)> 0 and not stoppedAtTL and abs(length2-length)==0:
				fuel2 = res[r-1][2]
				q= "insert into "+IDLEDATA+" values (" + str(v[0]) + ", " + str(abs(t-s)) + "," + str(abs(fuel2-fuel)) + ",'" + str(startTime) + "','" + str(res[r-1][0]) + "'," + str(abs(length2-length)) + ", " + str(res[r-1][3]) + ");"
				con.query(q)
#				print q
			stoppedAtTL = False
			s = -1
			fuel = 0
			length = 0
		if res[r][1] == 1 and s== -1:
			s = time.mktime(time.strptime(res[r][0], "%Y-%m-%j %H:%M:%S"))
			startTime = res[r][0]
			fuel = res[r][2]
			length = res[r][5]

con.query("DROP INDEX IF EXISTS vehicleid_" + DATATABLE + "_idx;Create index vehicleid_" + IDLEDATA + "_idx on " + IDLEDATA + " (vehicleid);")
con.query("DROP INDEX IF EXISTS stopped_" + DATATABLE + "_idx;Create index stopped_" + IDLEDATA + "_idx on " + IDLEDATA + " (stopped);")
con.query("DROP INDEX IF EXISTS fuel_" + DATATABLE + "_idx;Create index fuel_" + IDLEDATA + "_idx on " + IDLEDATA + " (fuel);")
con.query("DROP INDEX IF EXISTS startTime_" + DATATABLE + "_idx;Create index startTime_" + IDLEDATA + "_idx on " + IDLEDATA + " (startTime);")
con.query("DROP INDEX IF EXISTS length_" + DATATABLE + "_idx;Create index length_" + IDLEDATA + "_idx on " + IDLEDATA + " (length);")
	

print "Finding idle periods with " + str(duration) + " seconds duration"
con.query('alter table ' + DATATABLE + ' drop IF EXISTS idle;')
con.query('alter table ' + DATATABLE + ' add column idle int not null default 0;')

vehicles = con.query("select distinct vehicleid from "+ DATATABLE + ";").getresult()
for v in vehicles:
	print "Processing vehicle " + str(v[0])
	res = con.query("select timestamp, stopped, totalconsumed, tid, tl from " + DATATABLE + " where vehicleid=" + str(v[0]) +" and dirty is false order by timestamp;").getresult()
	s = -1
	fuel = 0
	stoppedAtTL = False 			
	for r in range(0, len(res)-1):
		if res[r][1]==1 and not res[r][4] == None:
			stoppedAtTL = True
#		print str(res[r][3]) + " " + str(res[r][0]) + " " + str(stoppedAtTL) + " " + str(type(res[r][4])) + " " + str(res[r][1])
		if (res[r][1] == 0 or ((r==len(res)-1 or not res[r-1][3]== res[r][3]) and res[r][1] == 1)) and not s==-1 and r > 0:
#			print "end"
			t = time.mktime(time.strptime(res[r-1][0], "%Y-%m-%j %H:%M:%S"))
			if abs(t-s)> duration and not stoppedAtTL:
				fuel2 = res[r-1][2]
#				q= "insert into "+IDLEDATA+" values (" + str(v[0]) + ", " + str(abs(t-s)) + "," + str(abs(fuel2-fuel)) + ",'" + str(startTime) + "')"
				q= "update " + DATATABLE + " set idle=1 where tid="+ str(res[r-1][3]) + " and timestamp >='" + str(startTime) + "' and timestamp <='" + str(res[r-1][0]) +"';"
				con.query(q)
#				print q
			stoppedAtTL = False
			s = -1
			fuel = 0
		if res[r][1] == 1 and s== -1:
			s = time.mktime(time.strptime(res[r][0], "%Y-%m-%j %H:%M:%S"))
			startTime = res[r][0]
			fuel = res[r][2]

con.query("DROP INDEX IF EXISTS idle_" + DATATABLE + "_idx; Create index idle_" + DATATABLE + "_idx on " + DATATABLE + " (idle);")	
	





print 'Percentage in idle'
con.query('alter table ' + TRIPDATA + ' drop if exists idle_percentage;')
con.query('alter table ' + TRIPDATA + ' add idle_percentage float;')
con.query('update ' + TRIPDATA + ' set idle_percentage = p from (select tid, count(case when idle=1 then 1 end)::float/count(*) as p from ' + DATATABLE + ' where dirty is false group by tid)f where ' + TRIPDATA + '.tid=f.tid;')



print 'Time in idle'
con.query('alter table ' + TRIPDATA + ' drop if exists idle_time;')
con.query('alter table ' + TRIPDATA + ' add idle_time float;')
trips = con.query('select distinct tid from ' + TRIPDATA).getresult()
for t in trips:
	trip = t[0]

	res = con.query("select timestamp, idle from " + DATATABLE + " where tid=" + str(trip) + " and dirty is false order by timestamp;").getresult()
	start = ""
	sek = 0
	for i in range(0,len(res)):
		ts = res[i][0]
		idle = res[i][1]
		if idle == 1 and (start == "" or i==0):
			start = ts
		if start != "" and (idle != 1 or i==len(res)-1):
			end = res[i-1][0]
			if i==len(res)-1:
				end = res[i][0]
			sek += abs(time.mktime(time.strptime(start, "%Y-%m-%j %H:%M:%S")) - time.mktime(time.strptime(end, "%Y-%m-%j %H:%M:%S"))) + 1
			start = ""
	con.query("update "+ TRIPDATA + " set idle_time = " + str(sek) + " where tid="+ str(trip) + ";")



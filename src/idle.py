import os, pg, math, sys, time
#1 = idle
USER = 'd103'
DB = 'gps_can'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

test= False

try:
	DATATABLE = sys.argv[1] + "_gps_can_data"
	IDLEDATA = sys.argv[1] + "_idledata"
	TRIPDATA = sys.argv[1] + "_trip_data"
	duration = sys.argv[2]
	if(len(sys.argv) > 3 and sys.argv[3]=="Test"):
		test = True
except:
	print 'Error: remember the parameters'
	exit(1)

if not test:
	print "Altering table"
	con.query('alter table ' + DATATABLE + ' drop IF EXISTS idle;')
	con.query('alter table ' + DATATABLE + ' add column idle int not null default 0;')



print 'Idle state with ' + str(duration) + " seconds duration"
trips = con.query('select distinct tid from ' + DATATABLE +' where tid is not null').getresult()
for t in trips:
	trip = t[0]
	res = con.query("select timestamp, speed, rpm from " + DATATABLE + " where tid=" + str(trip) + " and dirty is false order by timestamp;").getresult() #
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
			if sek >= duration:
				q= "update " + DATATABLE + " set idle=1 where tid="+ str(trip) + " and timestamp >='" +start + "' and timestamp <='" + end +"';"
				if not test:
					con.query(q)			
				
			start = ""
if not test:
	print "Creating index"
	con.query("Create index idle_" + DATATABLE + "_idx on " + DATATABLE + " (idle);")




if test:
	print "Counting idle"
	output = open('data/idleDuration.csv', 'a')
	temp = con.query("select count(*) from " + DATATABLE + " where idle=1;").getresult()[0][0];
	print >> output, str(duration) + " " + str(temp)
	print str(duration) + " " + str(temp)
	
	
	
	
	
if not test:
	print "Altering table"
	con.query('alter table ' + DATATABLE + ' drop IF EXISTS idleRange;')
	con.query('alter table ' + DATATABLE + ' add column idleRange int not null default 0;')

	con.query('update ' + DATATABLE + ' set idleRange = 1 where rpm>0 and speed = 0;')

	print "Creating index"
	con.query("DROP INDEX IF EXISTS idle_" + DATATABLE + "_idx;")
	con.query("Create index idle_" + DATATABLE + "_idx on " + DATATABLE + " (idleRange);")





	con.query("drop table if exists "+IDLEDATA+";")
	con.query("create table "+IDLEDATA+" (vehicleid bigint, idleRange int, fuel float, starTime timestamp);")
	print "Calculating"
	vehicles = con.query("select distinct vehicleid from "+ DATATABLE + ";").getresult()

	for v in vehicles:
		res = con.query("select timestamp, idleRange, totalconsumed, tid from " + DATATABLE + " where vehicleid=" + str(v[0]) +" and dirty is false order by timestamp;").getresult()
		s = -1
		fuel = 0
		for r in range(0, len(res)-1):		
			if (res[r][1] == 0 or ((r==len(res)-1 or not res[r-1][3]== res[r][3]) and res[r][1] == 1)) and not s==-1 and r > 0:
				t = time.mktime(time.strptime(res[r-1][0], "%Y-%m-%j %H:%M:%S"))
				if abs(t-s)> 0:
					fuel2 = res[r-1][2]
					con.query("insert into "+IDLEDATA+" values (" + str(v[0]) + ", " + str(abs(t-s)) + "," + str(abs(fuel2-fuel)) + ",'" + str(startTime) + "')")
				s = -1
				fuel = 0
			if res[r][1] == 1 and s== -1:
				s = time.mktime(time.strptime(res[r][0], "%Y-%m-%j %H:%M:%S"))
				startTime = res[r][0]
				fuel = res[r][2]



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



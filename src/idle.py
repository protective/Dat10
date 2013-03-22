import os, pg, math, sys, time
#1 = idle
USER = 'd103'
DB = 'gps_can'
DATATABLE = 'b_gps_can_data'
TRIPDATA = 'b_trip_data'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

test= False
duration = 0
if len(sys.argv) > 1:
	duration = int(sys.argv[1])


"""print "Altering table"
con.query('alter table ' + DATATABLE + ' drop IF EXISTS idle;')
con.query('alter table ' + DATATABLE + ' add column idle int not null default 0;')

print 'Setting idle state with ' + str(duration) + " seconds duration"
trips = con.query('select distinct tid from ' + DATATABLE ).getresult()
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
				con.query(q)			
				
			start = ""

print "Creating index"
con.query("Create index idle_" + DATATABLE + "_idx on " + DATATABLE + " (idle);")

if test:
	print "Counting idle"
	output = open('data/idleDuration.csv', 'a')
	temp = con.query("select count(*) from " + DATATABLE + " where idle=1;").getresult()[0][0];
	print >> output, str(duration) + " " + str(temp)
	print str(duration) + " " + str(temp)

print 'Percentage in idle'
con.query('alter table ' + TRIPDATA + ' drop if exists idle_percentage;')
con.query('alter table ' + TRIPDATA + ' add idle_percentage float;')
con.query('update ' + TRIPDATA + ' set idle_percentage = p from (select tid, count(case when idle=1 then 1 end)::float/count(*) as p from ' + DATATABLE + ' where dirty is false group by tid)f where ' + TRIPDATA + '.tid=f.tid;')
"""
print 'Time in idle'
con.query('alter table ' + TRIPDATA + ' drop if exists idle_time;')
con.query('alter table ' + TRIPDATA + ' add idle_time float;')
trips = con.query('select distinct tid from ' + TRIPDATA).getresult() #
for t in trips:
	trip = t[0]
	if str(trip)=='773':
		print '******************************************'

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



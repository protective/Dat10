import pg , math, sys, os ,time

USER = 'd103'
DB = 'gps_can'


try:
	SIZE = int(sys.argv[1])
	TIME = int(sys.argv[2])
	PREFIX = sys.argv[3]
except:
	print 'Error: remember the parameters'
	exit(1)

DATATABLE = PREFIX+"_gps_can_data"
TRIPDATA = PREFIX+"_trip_data"
CRUISEDATA = PREFIX+"_cruise_data"

test = False
if len(sys.argv) > 4:
	test = True
	filename = str(sys.argv[4])



print "Connecting to " + DB
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')


if not test:
	con.query('alter table ' + DATATABLE + ' drop IF EXISTS cruise;')
	con.query('alter table '+DATATABLE+' add column cruise bool default false;')
	con.query('drop table if exists ' + CRUISEDATA+";" )
	con.query("create table "+CRUISEDATA+" (vehicleid bigint, tid int, time int, fuel float, startTime timestamp, endTime timestamp);")


print "Extracting data"
res = con.query('select speedMod, timestamp, tid, vehicleid, totalconsumed  from ' + DATATABLE + ' where dirty is false order by vehicleid, timestamp').getresult()

cruiseBegin = 0
cruiseCur = 0
cruiseSpeed = 0

counter = 0
masterCounter = 0

Time = time.mktime(time.strptime(res[0][1], "%Y-%m-%j %H:%M:%S"))
while cruiseBegin < len(res) -1:
	cruiseCur += 1
	if cruiseCur < len(res) and cruiseSpeed <= res[cruiseCur][0] +SIZE and cruiseSpeed >= res[cruiseCur][0] -SIZE and cruiseSpeed > 0 and res[cruiseCur][0] > 0 and res[cruiseBegin][2] == res[cruiseCur][2]:
		#we are within thresshold of cruisespeed
		counter += 1
		continue
	else:
		if abs(Time-time.mktime(time.strptime(res[cruiseCur-1][1], "%Y-%m-%j %H:%M:%S"))) > TIME: #  
			#we have been using cc until now update
			if test:
				masterCounter += counter
			else:
				s1 = 'update ' + str(DATATABLE) + ' set cruise = true where tid = ' + str(res[cruiseBegin][2]) + ' and timestamp >= \''+str(res[cruiseBegin][1]) + '\' and timestamp <= \''+ str(res[cruiseCur-1][1]) + '\';'  
				con.query(s1)
				
				fuel = float(res[cruiseCur-1][4])-float(res[cruiseBegin][4])
				diffTime = time.mktime(time.strptime(res[cruiseCur-1][1], "%Y-%m-%j %H:%M:%S")) - time.mktime(time.strptime(res[cruiseBegin][1], "%Y-%m-%j %H:%M:%S"))
				s2= 'insert into ' + str(CRUISEDATA) + ' values (' + str(res[cruiseBegin][3]) + ', ' + str(res[cruiseBegin][2]) + ', ' + str(diffTime) + ', ' + str(fuel) + ", '" + str(res[cruiseBegin][1]) + "', '" + str(res[cruiseCur-1][1]) + "');"
				con.query(s2)
			cruiseBegin = cruiseCur-1
		
		cruiseBegin += 1
		cruiseCur = cruiseBegin
		cruiseSpeed = res[cruiseBegin][0]
		Time = time.mktime(time.strptime(res[cruiseBegin][1], "%Y-%m-%j %H:%M:%S"))
		counter = 0

if test:
	output = open('data/'+filename, 'a')
	ss = str(TIME) + " " + str(masterCounter)
	print ss 
	print >> output, ss

"""
if not test:
	print 'Percentage in cruise'
	con.query('alter table ' + TRIPDATA + ' drop if exists cruise_percentage;')
	con.query('alter table ' + TRIPDATA + ' add cruise_percentage float;')
	con.query('update ' + TRIPDATA + ' set cruise_percentage = p from (select tid, (count(*)-count(case when cruise =false then 1 end))::float/count(*) as p from ' + DATATABLE + ' where dirty is false group by tid)f where ' + TRIPDATA + '.tid=f.tid;')
"""





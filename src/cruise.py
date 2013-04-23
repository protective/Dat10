import pg , math, sys, os ,time

USER = 'd103'
DB = 'gps_can'

PREFIX = 'a'

SIZE = int(sys.argv[1])
TIME = int(sys.argv[2])
if len(sys.argv) > 3:
	PREFIX = sys.argv[3]
DATATABLE = ""+PREFIX+"_gps_can_data"
TRIPDATA = ""+PREFIX+"_trip_data"

test = False
if len(sys.argv) > 4:
	test = True
	filename = str(sys.argv[4])



print "Connecting to " + DB
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')


if not test:
	con.query('alter table ' + DATATABLE + ' drop IF EXISTS cruise;')
	con.query('alter table '+DATATABLE+' add column cruise bool default false;')


print "Extracting data"
res = con.query('select speedMod, timestamp, tid  from ' + DATATABLE + ' where dirty is false order by vehicleid, timestamp').getresult()

cruiseBegin = 0
cruiseCur = 0
cruiseSpeed = 0

counter = 0
masterCounter = 0

Time = time.mktime(time.strptime(res[0][1], "%Y-%m-%j %H:%M:%S"))
while cruiseBegin < len(res) -1:
	cruiseCur += 1
	if cruiseCur < len(res) and cruiseSpeed <= res[cruiseCur][0] +SIZE and cruiseSpeed >= res[cruiseCur][0] -SIZE and cruiseSpeed > 0 and res[cruiseBegin][2] == res[cruiseCur][2]:
		#we are within thresshold of cruisespeed
		counter += 1
		continue
	else:
		if abs(Time-time.mktime(time.strptime(res[cruiseCur-1][1], "%Y-%m-%j %H:%M:%S"))) > TIME: #  
			#we have been using cc until now update
			s = 'update ' + str(DATATABLE) + ' set cruise = true where tid = ' + str(res[cruiseBegin][2]) + ' and timestamp >= \''+str(res[cruiseBegin][1]) + '\' and timestamp <= \''+ str(res[cruiseCur-1][1]) + '\';'  
			if test:
				masterCounter += counter
			else:
				con.query(s)
		if cruiseCur >= len(res):
			break
		cruiseBegin = cruiseCur
		cruiseSpeed = res[cruiseBegin][0]
		Time = time.mktime(time.strptime(res[cruiseBegin][1], "%Y-%m-%j %H:%M:%S"))
		counter = 0

if test:
	output = open('data/'+filename, 'a')
	ss = str(TIME) + " " + str(masterCounter)
	print ss 
	print >> output, ss

if not test:
	print 'Percentage in cruise'
	con.query('alter table ' + TRIPDATA + ' drop if exists cruise_percentage;')
	con.query('alter table ' + TRIPDATA + ' add cruise_percentage float;')
	con.query('update ' + TRIPDATA + ' set cruise_percentage = p from (select tid, (count(*)-count(case when cruise =false then 1 end))::float/count(*) as p from ' + DATATABLE + ' where dirty is false group by tid)f where ' + TRIPDATA + '.tid=f.tid;')






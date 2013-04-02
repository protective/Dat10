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



con.query('alter table ' + DATATABLE + ' drop IF EXISTS cruise;')
con.query('alter table '+DATATABLE+' add column cruise bool default false;')


print "Extracting data"
res = con.query('select speed, timestamp, tid  from ' + DATATABLE + ' where dirty is false order by vehicleid, timestamp').getresult()
print "all done"

cruiseBegin = 0
cruiseCur = 0
cruiseSpeed = 0
noobs = 0
Time = time.mktime(time.strptime(res[0][1], "%Y-%m-%j %H:%M:%S"))
while cruiseBegin < len(res) -1:
	cruiseCur += 1
	noobs += 1
	if cruiseCur < len(res) and cruiseSpeed <= res[cruiseCur][0] +SIZE and cruiseSpeed >= res[cruiseCur][0] -SIZE and cruiseSpeed > 5 and res[cruiseBegin][2] == res[cruiseCur][2]:
		#we are within thresshold of cruisespeed

		continue
	else:
		if (abs(Time-time.mktime(time.strptime(res[cruiseCur-1][1], "%Y-%m-%j %H:%M:%S"))) > TIME and noobs >= 10):
			#we have been using cc until now update
			s = 'update ' + str(DATATABLE) + ' set cruise = true where tid = ' + str(res[cruiseBegin][2]) + ' and timestamp >= \''+str(res[cruiseBegin][1]) + '\' and timestamp <= \''+ str(res[cruiseCur-1][1]) + '\';'  
			con.query(s)
		
		cruiseBegin = cruiseCur
		cruiseSpeed = res[cruiseBegin][0]
		Time = time.mktime(time.strptime(res[cruiseBegin][1], "%Y-%m-%j %H:%M:%S"))
		noobs = 0


print 'Percentage in cruise'
con.query('alter table ' + TRIPDATA + ' drop if exists cruise_percentage;')
con.query('alter table ' + TRIPDATA + ' add cruise_percentage float;')
con.query('update ' + TRIPDATA + ' set cruise_percentage = p from (select tid, (count(*)-count(case when cruise =false then 1 end))::float/count(*) as p from ' + DATATABLE + ' where dirty is false group by tid)f where ' + TRIPDATA + '.tid=f.tid;')

res = con.query('select avg(cruise_percentage) from ' + TRIPDATA + ';').getresult()

output = open('data/'+filename, 'a')
ss = str(SIZE) + " " + str(res[0][0]) + ""
print ss 
print >> output, ss




import os, pg, math, sys, time
#1 = idle
USER = 'd103'
DB = 'gps_can'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

test= False
PREFIX = 'a'
if len(sys.argv) > 1:
	PREFIX = sys.argv[1]
DATATABLE = ""+PREFIX+"_gps_can_data"
TRIPDATA = ""+PREFIX+"_trip_data"

"""
print "Altering table"
con.query('alter table ' + DATATABLE + ' drop IF EXISTS idleRange;')
con.query('alter table ' + DATATABLE + ' add column idleRange int not null default 0;')

con.query('update ' + DATATABLE + ' set idleRange = 1 where rpm>0 and speed = 0;')

print "Creating index"
con.query("DROP INDEX IF EXISTS idle_" + DATATABLE + "_idx;")
con.query("Create index idle_" + DATATABLE + "_idx on " + DATATABLE + " (idleRange);")

"""

con.query("drop table if exists vehicleIdleRange;")
con.query("create table vehicleIdleRange (vehicleid bigint, idleRange int, fuel float);")
print "Calculating"
vehicles = con.query("select distinct vehicleid from "+ DATATABLE + ";").getresult()

for v in vehicles:
	res = con.query("select timestamp, idleRange, totalconsumed from " + DATATABLE + " where vehicleid=" + str(v[0]) +" order by timestamp;").getresult()
	s = -1
	fuel = 0
	for r in range(0, len(res)-1):
		if res[r][1] == 1 and s== -1:
			s = time.mktime(time.strptime(res[r][0], "%Y-%m-%j %H:%M:%S"))
#			print res[r][0]
			fuel = res[r][2]
		if r > 0:
			timeDiff = abs(time.mktime(time.strptime(res[r-1][0], "%Y-%m-%j %H:%M:%S")) - time.mktime(time.strptime(res[r][0], "%Y-%m-%j %H:%M:%S")))
		else:
			timeDiff = 0
		if (res[r][1] == 0 or ((r==len(res)-1 or timeDiff > 90) and res[r][1] == 1)) and not s==-1 and r > 0:
			t = time.mktime(time.strptime(res[r-1][0], "%Y-%m-%j %H:%M:%S"))
			if abs(t-s)> 0:
#				if abs(t-s)>50000:
#					print str(r) + "\t" + str(res[r][1]) + "\t" + str(timeDiff) +"\t" + str(s) + "\t" + str(t) + "\t" + str(abs(t-s)) + "\t" + res[r-1][0] + "\t" + str(v[0])
#					break
				fuel2 = res[r-1][2]
				if fuel2 > 4294000:
					fuel2 = res[r-2][2]
				con.query("insert into vehicleIdleRange values (" + str(v[0]) + ", " + str(abs(t-s)) + "," + str(abs(fuel2-fuel)) + ")")
			s = -1
			fuel = 0

		



if test:
	print "Counting idle"
	output = open('data/idleDuration.csv', 'a')
	temp = con.query("select count(*) from " + DATATABLE + " where idle=1;").getresult()[0][0];
	print >> output, str(duration) + " " + str(temp)
	print str(duration) + " " + str(temp)

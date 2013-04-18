import os, pg, math, sys, time
#1 = idle
USER = 'd103'
DB = 'gps_can'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

test= False

try:
	DATATABLE = sys.argv[1] + "_gps_can_data"
	diff = int(sys.argv[2])
except:
	print 'Error: remember the parameters'
	exit(1)

counter = 0
trips = con.query('select distinct tid from ' + DATATABLE +' where tid is not null').getresult()
for t in trips:
	stop = False
	trip = t[0]
	res = con.query("select speed, timestamp from " + DATATABLE + " where tid=" + str(trip) + " and dirty is false order by timestamp;").getresult()
	for r in range (1, len(res)-2):
		if int(res[r][0]) == 0 and res[r-1][0]>diff and res[r+1][0]>diff:
#			print "dirty " + str(trip) + " " + str(res[r][1])
			counter += 1

output = open('data/testSpeed.csv', 'a')
print >> output, str(diff) + " " + str(counter)

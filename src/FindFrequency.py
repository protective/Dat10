import os, pg, math, sys, time
#1 = idle
USER = 'd103'
DB = 'gps_can'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

try:
	DATATABLE = sys.argv[1]
except:
	print 'Error: remember the parameters'
	exit(1)

output = open('data/freqencyTest.csv', 'w+')
vehicles = con.query("select distinct vehicleid from "+ DATATABLE + ";").getresult()
counter = 0;

for v in vehicles:
	res = con.query("select timestamp from " + DATATABLE + " where vehicleid=" + str(v[0]) +" and dirty is false order by timestamp;").getresult()
	p = time.mktime(time.strptime(res[0][0], "%Y-%m-%j %H:%M:%S"))
	for r in res:
		c = time.mktime(time.strptime(r[0], "%Y-%m-%j %H:%M:%S"))
		if abs(p-c) > 1:
			counter +=1;
		p=c
		

	print >> output, str(v[0]) + " " + str(counter)
	print str(v[0]) + " " + str(counter)
	counter=0

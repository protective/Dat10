import pg, sys,os

USER = os.getlogin()
DB = 'gps_can'
OLD_TABLE = 'a_gps_can_data'
TABLE = 'trip_data'

print "Connecting to " + DB
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

fuelprl = con.query('select vehicleid, avg(km_pr_l) from trip_data where km_pr_l is not null group by vehicleid order by avg desc;').getresult()

idleTime = con.query('select vehicleid, count(case when idle=1 then 1 end) as idle from a_gps_can_data group by vehicleid order by idle;').getresult()

result = {}
nmin = 0
nmax = 100

#print "fuel pr l"
omax= fuelprl[0][1]
omin= fuelprl[0][1]
for r in fuelprl:
	if r[1]> omax:
		omax = r[1]
	if r[1]<omin:
		omin=r[1]
	
for r in fuelprl:
	val = nmax-(((r[1]-omin) * (nmax-nmin)) / (omax-omin) + nmin)
	#print str(r[0]) + '\t' + str(r[1]) + '\t' + str(val)
	result[r[0]] = val

#print "idle time"
omax= idleTime[0][1]
omin= idleTime[0][1]
for r in idleTime:
	if r[1]> omax:
		omax = r[1]
	if r[1]<omin:
		omin=r[1]
	
for r in idleTime:
	val = ((r[1]-omin) * (nmax-nmin)) / (omax-omin) + nmin
	#print str(r[0]) + '\t' + str(r[1]) + '\t' + str(val)
	result[r[0]] += val
	
#print "result"
for r in sorted(result, key=result.get):
	print str(r) + "\t" + str(result[r])

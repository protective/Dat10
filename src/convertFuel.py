import random, time, math, pg, sys,os

USER = os.getlogin()
DB = sys.argv[1]
TABLE = sys.argv[2]

print "Connecting to " + DB
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

#con.query('alter table ' + TABLE + ' add column fuel float;')

print "Fetching data"
res = con.query('select totalconsumed, timestamp, tid from ' + TABLE + ' where dirty is null order by tid, timestamp').getresult()

prevTime = time.mktime(time.strptime(res[0][1], "%Y-%m-%j %H:%M:%S"))
prevFuel = res[0][0]

for p in range(0, len(res)):
	#Reset when new tid
	diffFuel = res[p][0]-prevFuel
	diffTime = time.mktime(time.strptime(res[p][1], "%Y-%m-%j %H:%M:%S"))-prevTime
	
	if diffTime > 0:
		fuel = diffFuel/diffTime
	else:
		fuel = diffFuel
		
	query = 'update ' + TABLE + ' set fuel=' + str(fuel) + ' where tid=' + str(res[p][2]) + ' and timestamp=' + str(res[p][1]) + ';'
	print query
	
	prevFuel = res[p][0]
	prevTime = time.mktime(time.strptime(res[p][1], "%Y-%m-%j %H:%M:%S"))
	
	if p > 10:
		break

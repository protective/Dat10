import pg , math, sys, os ,time

USER = os.getlogin()
DB = sys.argv[1]
TABLE = sys.argv[2]

print "Connecting to " + DB
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')


try:
	con.query('alter table '+TABLE+' add column cruise bool;')
except:
	print "already exist"

#con.query('update ' + TABLE + ' set cruise = false;') 
print "done update to false"
res = con.query('select speed, timestamp  from ' + TABLE + ' order by vehicleid, timestamp').getresult()
print "all done"

cruiseBegin = 0;
cruiseCur = 0;
cruiseSpeed = 0;
Time = time.mktime(time.strptime(res[0][1], "%Y-%m-%j %H:%M:%S"))
while cruiseBegin < len(res):
	if cruiseSpeed <= res[cruiseCur][0] +1 and cruiseSpeed >= res[cruiseCur][0] -1 and cruiseSpeed > 5:
		#we are within thresshold of cruisespeed
		cruiseCur += 1
		continue
	else:
		if (abs(Time-time.mktime(time.strptime(res[cruiseCur][1], "%Y-%m-%j %H:%M:%S"))) > 10):
			#we have been using cc until now update
			print "update"
			con.query('update ' + TABLE + ' set cruise = true where timestamp >= \''+res[cruiseBegin][1] + '\' and timestamp <= \''+ res[cruiseCur][1] + '\';'  )
		
		cruiseBegin += 1
		cruiseCur = cruiseBegin;
		cruiseSpeed = res[cruiseBegin][0]
		Time = time.mktime(time.strptime(res[cruiseBegin][1], "%Y-%m-%j %H:%M:%S"))
		








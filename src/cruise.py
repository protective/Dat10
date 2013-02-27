import pg , math, sys, os ,time

USER = os.getlogin()
DB = 'gps_can'
TABLE = 'a_gps_can_data'

print "Connecting to " + DB
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')



con.query('alter table ' + TABLE + ' drop IF EXISTS cruise;')
con.query('alter table '+TABLE+' add column cruise bool default false;')


print "Extracting data"
res = con.query('select speed, timestamp, tid  from ' + TABLE + ' where dirty is null order by vehicleid, timestamp').getresult()
print "all done"

cruiseBegin = 0
cruiseCur = 0
cruiseSpeed = 0
noobs = 0
Time = time.mktime(time.strptime(res[0][1], "%Y-%m-%j %H:%M:%S"))
while cruiseBegin < len(res) -1:
	cruiseCur += 1
	noobs += 1
	if cruiseCur < len(res) and cruiseSpeed <= res[cruiseCur][0] +1 and cruiseSpeed >= res[cruiseCur][0] -1 and cruiseSpeed > 5 and res[cruiseBegin][2] == res[cruiseCur][2]:
		#we are within thresshold of cruisespeed

		continue
	else:
		if (abs(Time-time.mktime(time.strptime(res[cruiseCur-1][1], "%Y-%m-%j %H:%M:%S"))) > 45 and noobs >= 10):
			#we have been using cc until now update
			s = 'update ' + str(TABLE) + ' set cruise = true where tid = ' + str(res[cruiseBegin][2]) + ' and timestamp >= \''+str(res[cruiseBegin][1]) + '\' and timestamp <= \''+ str(res[cruiseCur-1][1]) + '\';'  
			print s
			con.query(s)
		
		cruiseBegin = cruiseCur
		cruiseSpeed = res[cruiseBegin][0]
		Time = time.mktime(time.strptime(res[cruiseBegin][1], "%Y-%m-%j %H:%M:%S"))
		noobs = 0








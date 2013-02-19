import pg , math, sys

DB = sys.argv[1]
TABLE = sys.argv[2]

con = pg.connect(dbname=DB, host='localhost', user='karsten',passwd='F1ff')

try:
	con.query('alter table '+TABLE+' add column cruise bool;')
finally:
	print "begin"

res = con.query('select speed, timestamp  from ' + TABLE + ' order by vehicleid, timestamp').getresult()
con.query('update ' + TABLE + ' set cruise = false;') 

cruiseBegin = 0;
cruiseCur = 0;
cruiseSpeed = 0;
Time
while cruiseBegin < len(res)
	if cruiseSpeed <= res[cruiseBegin][0] +1 and cruiseSpeed >= res[cruiseBegin][0] -1 and cruiseSpeed > 5:
		#we are within thresshold of cruisespeed
		cruiseCur += 1
		continue
	else
		if (abs(Time-time.mktime(time.strptime(res[cruiseBegin][1], "%Y-%m-%j %H:%M:%S"))) > 10)
			#we have been using cc until now update
			res = con.query('update ' + TABLE + ' set cruise = true where timestamp >= '+res[cruiseBegin][1] + ' and timestamp <= '+ res[cruiseCur][1] + ';'  ).getresult()
			
		cruiseBegin += 1
		cruiseCur = cruiseBegin;
		cruiseSpeed = res[cruiseBegin][0]
		Time = time.mktime(time.strptime(res[cruiseBegin][1], "%Y-%m-%j %H:%M:%S"))
		








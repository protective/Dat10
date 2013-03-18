import pg , math, sys, os ,time

USER = 'karsten'
DB = "gps_can"
QUERY_TABLE = "a_gps_can_data"
TABLE = "trip_data"

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

con.query("alter table " + TABLE + " drop IF EXISTS TlCounter;")
con.query('alter table ' + TABLE + ' add TlCounter int not null default 0;')

con.query("alter table " + TABLE + " drop IF EXISTS TlRedCounter;")
con.query('alter table ' + TABLE + ' add TlRedCounter int not null default 0;')

con.query("alter table " + TABLE + " drop IF EXISTS TlGreenCounter;")
con.query('alter table ' + TABLE + ' add TlGreenCounter int not null default 0;')

res = con.query('select speed, timestamp, tid, tl  from ' + QUERY_TABLE + ' where tid in (select tid from ' + TABLE + ')order by tid, timestamp').getresult()




TlCounter = 0
TlRedCounter = 0
TlGreenCounter = 0

stopping = 0;
inlight = False;
i = 0
tid = 0
tid = res[0][2]
oldlight = 0
while i <= len(res):
	if(tid == res[i][2] and i < len(res)):
		print res[i]
		
		if inlight == False and res[i][3]:
			oldlight = res[i][3]
			inlight = True
			TlCounter += 1

		if stopping < 2 and inlight==True and res[i][0] == 0 and i > 0 and res[i-1][0] == 0:
			stopping += 1
			if stopping == 2:
				TlRedCounter+= 1
		
		if inlight == True and stopping <= 1 and (not res[i][3] or oldlight != res[i][3]):
			inlight = False
			TlGreenCounter +=1
			
		if not res[i][3] or oldlight != res[i][3]:
			inlight = False
			stopping = 0

			
	else:
		print "conunter " + str(TlCounter) + " green " + str(TlGreenCounter) + " red " + str(TlRedCounter)
		TlCounter = 0
		TlRedCounter = 0
		TlGreenCounter = 0
		tid = res[i][2]
	i+=1


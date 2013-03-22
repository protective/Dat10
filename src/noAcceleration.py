import pg , math, sys, os ,time

USER = 'd103'
DB = "gps_can"
PREFIX = 'a'
if len(sys.argv) > 1:
	PREFIX = sys.argv[1]
QUERY_TABLE = ""+PREFIX+"_gps_can_data"
TABLE = ""+PREFIX+"_trip_data"



con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

con.query("alter table " + TABLE + " drop IF EXISTS acckm;")
con.query('alter table ' + TABLE + ' add acckm float not null default 0;')

res = con.query('select speed, timestamp, tid  from ' + QUERY_TABLE + ' where tid in (select tid from ' + TABLE + ') and dirty is false order by tid, timestamp').getresult()

curSpeed = 0
oldSpeed = 0
acccounter = 0

tid = res[0][2]
i = 1

minbuff = 5
oldSpeed = res[0][0]
while i < len(res):
	if(tid == res[i][2] and i != len(res)-1):
		if(res[i][0] - oldSpeed > minbuff):
			acccounter+= (res[i][0] - oldSpeed) - minbuff
			oldSpeed = res[i][0] - minbuff
		elif(oldSpeed - res[i][0] > minbuff):
			oldSpeed = res[i][0] + minbuff
			
		i+=1
	else:
		temp = con.query('select total_km from ' + TABLE + ' where tid = '+ str(tid) ).getresult()
		total = 0
		if(float(temp[0][0] != 0)):
			total = float(acccounter)/ float(temp[0][0])
		s = "update " + TABLE + " set acckm = " + str(total) + " where tid = " + str(tid) + ";"
		con.query(s)
		acccounter = 0
		i+=1
		if(i != len(res)):
			tid = res[i][2]
			oldSpeed = res[i][0]




import pg , math, sys, os ,time

USER = os.getlogin()
DB = "gps_can"
TABLE = "a_gps_can_data"



con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

res = con.query('select speed, timestamp, tid  from ' + TABLE + ' where tid in (select tid from trip_data) order by tid, timestamp').getresult()

try:
	con.query('alter table '+TABLE+' add column acckm int;')
except:
	print "already exist"



curSpeed = 0
oldSpeed = 0
acccounter = 0

tid = res[0][2]
i = 1

minbuff = 5
oldSpeed = res[0][0]
while i < len(res):
	if(tid == res[i][2]):
		if(res[i][0] - oldSpeed > minbuff):
			acccounter+= (res[i][0] - oldSpeed) - minbuff
			oldSpeed = res[i][0] - minbuff
		elif(oldSpeed - res[i][0] > minbuff):
			oldSpeed = res[i][0] + minbuff
			
		i+=1
	else:
		temp = con.query('select total_km from trip_data where tid = '+ str(tid) ).getresult()
		total = 0
		if(temp[0][0] != 0):
			total = acccounter/ temp[0][0]
		s = "update trip_data set acckm = " + str(total) + " where tid = " + str(tid) + ";"
		#con.query(s)
		acccounter = 0
		i+=1
		tid = res[i][2]
		oldSpeed = res[i][0]




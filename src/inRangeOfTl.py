import pg , math, sys, os ,time

USER = "d103"
DB = "gps_can"

PREFIX = 'a'

SIZE = int(sys.argv[1])
if len(sys.argv) > 2:
	PREFIX = sys.argv[2]
DATATABLE = ""+PREFIX+"_gps_can_data"
TRIPDATA = ""+PREFIX+"_trip_data"


test = False
if len(sys.argv) > 3:
	test = True
	filename = str(sys.argv[3])


con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')


con.query("alter table " + DATATABLE + " drop IF EXISTS tl;")
con.query('alter table ' + DATATABLE + ' add tl int default null;')

res = con.query("select max(tid) from "+DATATABLE+"").getresult()
print res

for i in range(0,res[0][0]):
	con.query("update "+DATATABLE+" as "+PREFIX+" set tl = t.tlId from trafficlights as t where ST_Dwithin(t.geom,"+PREFIX+".geom,"+str(SIZE)+") and "+PREFIX+".tid = "+ str(i) + ";")
	print str(i) + " of " + str(res[0][0]) 


#"update a_gps_can_data as a set tl = t.tlId from trafficlights as t where ST_Dwithin(t.geom,a.geom,100)"

#"explain update a_gps_can_data as a set tl = t.tlId from (select tlId from trafficlights where ST_Dwithin(geom,a.geom,100) )t"

#print 'Percentage in idle wo_tl'
#con.query('alter table ' + TRIPDATA + ' drop if exists idle_wo_tl_percentage;')
#con.query('alter table ' + TRIPDATA + ' add idle_wo_tl_percentage float;')
#con.query('update ' + TRIPDATA + ' set idle_wo_tl_percentage = p from (select tid, count(case when idle=1 and tl is null then 1 end)::float/count(*) as p from ' + DATATABLE + ' where dirty is false group by tid)f where ' + TRIPDATA + '.tid=f.tid;')

#print 'Percentage in idle w_tl'
#con.query('alter table ' + TRIPDATA + ' drop if exists idle_w_tl_percentage;')
#con.query('alter table ' + TRIPDATA + ' add idle_w_tl_percentage float;')
#con.query('update ' + TRIPDATA + ' set idle_w_tl_percentage = p from (select tid, count(case when idle=1 and tl is not null then 1 end)::float/count(*) as p from ' + DATATABLE + ' where dirty is false group by tid)f where ' + TRIPDATA + '.tid=f.tid;')









con.query("alter table " + TRIPDATA + " drop IF EXISTS TlCounter;")
con.query('alter table ' + TRIPDATA + ' add TlCounter float not null default 0;')

con.query("alter table " + TRIPDATA + " drop IF EXISTS TlRedCounter;")
con.query('alter table ' + TRIPDATA + ' add TlRedCounter float not null default 0;')

con.query("alter table " + TRIPDATA + " drop IF EXISTS TlGreenCounter;")
con.query('alter table ' + TRIPDATA + ' add TlGreenCounter float not null default 0;')

res = con.query('select speed, timestamp, tid, tl  from ' + DATATABLE + ' where tid in (select tid from ' + TRIPDATA + ')order by tid, timestamp').getresult()


tcounter = float(0)
ttotalcounter = float(0)

TlCounter = float(0)
TlRedCounter = float(0)
TlGreenCounter = float(0)

stopping = 0;
inlight = False;
i = 0
tid = 0
tid = res[0][2]
oldlight = 0
while i <= len(res):
	if(i < len(res) and tid == res[i][2] ):
		#print res[i]
		
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
		#print "conunter " + str(TlCounter) + " green " + str(TlGreenCounter) + " red " + str(TlRedCounter)

		temp = con.query('select total_km from ' + TRIPDATA + ' where tid = '+ str(tid) ).getresult()
		total = 0		
		if(float(temp[0][0] != 0)):
			total = float(temp[0][0])
		if total > 0:
			#s = "update " + TRIPDATA + " set TlCounter = " + str(TlCounter/total) + " , TlRedCounter = " + str(TlRedCounter/total) + " , TlGreenCounter = " + str(TlGreenCounter/total) + " where tid = " + str(tid) + ";"
			tcounter +=1
			ttotalcounter += TlCounter/total
		#else: 
			#s = "update " + TRIPDATA + " set TlCounter = " + str(0) + " , TlRedCounter = " + str(0) + " , TlGreenCounter = " + str(0) + " where tid = " + str(tid) + ";"
		#print s
		#con.query(s)

		TlCounter = 0
		TlRedCounter = 0
		TlGreenCounter = 0
		if i < len(res):
			tid = res[i][2]
	i+=1



output = open('data/'+filename, 'a')
ss = str(SIZE) + " " + str(ttotalcounter/tcounter) + ""
print ss 
print >> output, ss










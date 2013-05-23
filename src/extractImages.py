import pg, sys, os, csv, time

USER = 'd103'
DB = 'gps_can'
TABLE = 'trip_data'
TYPE = sys.argv[1]
if len(sys.argv) > 2:
	TABLE = sys.argv[2]
path = ''

if (False):
	USER = 'sabrine'
	path = ''

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')


#clusters = [[3.5, 'Low', '1'], [8.125, 'Medium', '3'],[100, 'High', '2']]
#clusters = [4,7.7]
#clusters.append(con.query('select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+ TABLE + ';').getresult()[0][0])
#clusters.append(con.query('select avg(km_pr_l) from '+TABLE+' where km_pr_l > (select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+TABLE+')').getresult()[0][0])

noClasses= 3
clusters = [[3.5, 'Outliers', 13]]
r = con.query("select count(case when km_pr_l >=" + str(clusters[0][0]) + " then 1 end)::float/" + str(noClasses) + " from g_trip_data ;").getresult()
kmprl = con.query("select km_pr_l from g_trip_data where km_pr_l >=" + str(clusters[0][0]) + " order by km_pr_l;").getresult()
clusters.append([kmprl[int(r[0][0])][0], 'Low', '1'])
clusters.append([kmprl[int(r[0][0])*2][0], 'Medium', '9'])
clusters.append([100, 'High', '2']) #100 is dummy value


#Letter, color, pattern
patterns = {1: ['b', 'red', '1'], 2: ['c', 'blue', '2'], 3: ['a', 'green', '4'], 4: ['d', '#BB00FF', '5']}

if TYPE == 'showClusters':
	print clusters
	exit(1)

print "set terminal png size 800,400;"


def getTime(t):
	return float(time.mktime(time.strptime(t, "%Y-%m-%j %H:%M:%S")))


if TYPE == 'km_pr_l':
	vehicles = con.query("select distinct vehicleid from " + TABLE + ";").getresult()

	i = 0
	for v in vehicles:
		vid = str(v[0])
		res = con.query("select km_pr_l from " + TABLE + " where vehicleid=" + vid + " order by tid;").getresult()
		output = open(path + 'data/' + vid + '_kmldata.csv', 'wb')
		for r in res:
			print>> output, str(i) + " " + str(r[0])
			i+=1
 
	print "set output '" + path + "images/kmlTrips.png';"
	print "set ylabel 'Fuel efficiency (km/l)'"
	print "set xlabel 'Trips'"
	print "set yrange[0:12]"
	print "unset xtics"
	s = "plot "
	for v in vehicles:
		vid = str(v[0])
		s+= "'"+path + "data/" + vid + "_kmldata.csv' lc rgb '" + patterns[v[0]][1]+ "' title '" + vid + "', "

	for c in clusters:
		s += str(c[0])+" lw 2 lc rgb \"black\" notitle,"
	
	print s[:-1]
	#print s + ""+str(clusters[0])+" lw 2 lc rgb \"black\" notitle, "+str(clusters[1])+" lw 2 lc rgb \"black\" notitle"
	

elif TYPE == 'TripsKmlCluster':
	res = con.query("select round(km_pr_l::decimal*4,0)/4 as round, count(*) from " + TABLE + " group by round order by round;").getresult()
	output = open(path +'data/TripsKmlCluster.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for re in res:
		writer.writerow(re)

	print "set output '" + path + "images/TripsKmlCluster.png';"
	print "set ylabel 'Number of trips"
	print "set xlabel 'Fuel efficiency (km/l)'"
	print "set xtic 0.5"

	for i in clusters:
		print "set arrow from " + str(i[0]) + ",0 to " + str(i[0]) + ",300 lw 2 nohead"
	
	print "plot '" + path + "data/TripsKmlCluster.csv' with lines lw 3 notitle"


elif TYPE == 'TimeTrips':
	print "set output '" + path + "images/TimeTrips.png';"
	print "set ylabel 'Number of trips"
	print "set xlabel 'Timeframe (s)'"
	print "set yrange[0:]"
	print "set xrange[5:]"

	print "set arrow from 120,0 to 120,9569 lw 2 nohead"
	print "set arrow from 5,9569 to 120,9569,30 lw 2 nohead"
	print "plot '" + path + "data/trajectoryTime.csv' using 1:3 with lines lw 3 notitle"

elif TYPE == 'LengthTrips': 
	print "set output '" + path + "images/TripsLength.png';"
	print "set ylabel 'Number of trips"
	print "set xlabel 'Minimum number of records in trip	'"
	print "set yrange[0:]"
	print "set xtics 5"
	
	print "set arrow from 30,0 to 30,3509 lw 2 nohead"
	print "set arrow from 0,3509 to 30,3509,30 lw 2 nohead"
	print "plot '" + path + "data/trajectoryLength.csv' using 2:3 with lines lw 3 notitle"

elif TYPE == 'LengthTrips2': 
	print "set output '" + path + "images/TripsLength2.png';"
	print "set ylabel 'Number of trips"
	print "set xlabel 'Minimum trip length (#records)'"
	print "set yrange[0:]"
	print "set xtics 5"

	print "plot '" + path + "data/trajectoryLength2.csv' using 2:4 with lines lw 3 notitle"
	
elif TYPE == 'minFuel':
	print "set output '" + path + "images/minFuel.png';"
	print "set ylabel 'Number of trips"
	print "set xlabel 'Minimum fuel consumption'"
	output = open(path +'data/minFuel.csv', 'wb')
	for i in range(0,20, 1):
		step = float(i)/10
		res = con.query("select count(*)-count(case when total_fuel < " + str(step) + " then 1 end) from " + TABLE + ";").getresult()
		print >>output, str(step) + " " + str(res[0][0])

	print "plot '" + path + "data/minFuel.csv' with lines lw 3 notitle"

elif TYPE == 'TripLengthKml':
	res = con.query("select total_km, km_pr_l from " + TABLE + ";").getresult()
	output = open(path +'data/tripLengthKml.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for r in res:
		writer.writerow(r)

	
	print "set output '" + path + "images/TripLengthKml.png';"
	print "set ylabel 'km/l"
	print "set xlabel 'km'"

	print "plot '" + path + "data/tripLengthKml.csv' notitle"
elif TYPE == 'frequency':


	data = {}

	res = con.query("select timestamp, tid from g_gps_can_data  order by timestamp,tid ").getresult()
	


	output = open(path +'data/frequency.csv', 'wb')
	#writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	oldTime = None
	oldId = res[0][1]
	for i in res:
		if i[1] != oldId:
			oldTime = None
			oldId = i[1]
		if(oldTime != None):
			if not getTime(i[0])-oldTime in data:
				data[getTime(i[0])-oldTime] = 0
			data[getTime(i[0])-oldTime] += 1
		oldTime = getTime(i[0])

	#print data
	for k,v in data.items():
		output.write(str(k) + " " + str(v) + "\n")

	
	print "set output '" + path + "images/frequency.png';"
	print "set ylabel 'Number of records'"
	print "set xlabel 'Seconds (s)'"
	print "set xr[0.5:]"
	print "set style fill solid border -1"
	print "set boxwidth  1"
	print "set logscale y 10"
	print "plot '" + path + "data/frequency.csv' with boxes lw 1 notitle"



elif TYPE == 'trajectory':

	#segment1 =  '50037' #"542931"
	if sys.argv[3] == "1":
		segment1 = "542931"
		segment2 = "542894"
		geo = "ST_SetSRID(ST_MakePoint(9.0046,56.00939),4326)"
	elif sys.argv[3] == "2":
		segment1 = "553000"
		segment2 = "552999"
		geo = "ST_SetSRID(ST_MakePoint(9.03585,56.13387),4326)"
	elif sys.argv[3] == "3":
		segment1 = "542931"
		segment2 = "542894"
		geo = "ST_SetSRID(ST_MakePoint(9.0046,56.00939),4326)"


	res = con.query("select distinct a.tid , a.vehicleid from g_gps_can_data as a , g_gps_can_data as b where a.timestamp < b.timestamp and a.segmentkey = "+segment1+" and b.segmentkey = "+segment2+" and a.tid = b.tid order by a.vehicleid;").getresult()
	
	if sys.argv[3] == "3":
		res = [[10423,1],[10380,1],[9492,1],[7285,1],[6918,1]]
	toplot = []
	for i in res:

		low = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+" and segmentkey = "+segment1+") and tid = "+ str(i[0])+" ").getresult()

		high = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp  = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+"  and ST_DWithin(geom," + geo + ",50) and kmcounter <= "+str(low[0][2] + 2) +") and tid = "+ str(i[0])+" ").getresult()
				

		res2 = []		
		if len(high):
			res2 = con.query("select timestamp, speedMod from " + TABLE + " where timestamp >= '" + low[0][1] + "' and timestamp <= '" + high[0][1] + "' and tid = "+ str(i[0])+" order by timestamp").getresult()


		output = open(path +'data/trajectory/'+ str(i[0])+'.csv', 'wb')
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		
		if len(res2) > 0:
			begin = getTime(res2[0][0])
			#print high[0][2] - low[0][2]
			toplot.append([i[0], high[0][0] - low[0][0]])
			for r  in range(0,len(res2)):

				temp = str(getTime(res2[r][0]) - begin)
				#temp = res2[r][0] - begin
				res2[r] = list(res2[r])
				res2[r][0] = temp
				writer.writerow(res2[r])

	
	print "set output '" + path + "images/trajectory.png';"
	print "set ylabel 'Speed(km/t)'"
	print "set xlabel 'Time(s)'"
	print "set xr[0:]"
	s = "plot "

	legendset = {}

	toplot.sort(key=lambda tup: tup[1])

	for v in toplot:

		cou = 0
		if v[1]< 0.1:
			cou = 2
			legend = "[0, 0.1) l"
		elif v[1] < 0.14:
			cou = 3
			legend = "[0.1, 0.14) l"
		elif v[1] < 0.18:
			cou = 4
			legend = "[0.14, 0.18) l"
		elif v[1] < 0.22:
			cou = 9
			legend = "[0.18, 0.22) l"
		elif v[1] <= 0.26:
			cou = 13
			legend = "[0.22, 0.26] l"



		#s += "'"+  path + "data/trajectory/"+str(v[0])+".csv' using 1:2 with lines lc " + str(cou) + "  title '" + str(v[1]) +" l fuel"+ str(v[0]) + "',"
		#s += "'"+  path + "data/trajectory/"+str(v[0])+".csv' using 1:2 with lines lc " + str(cou) + "  notitle,"
		if not sys.argv[3] == "3":
			if(not cou in legendset):
				s += "'"+  path + "data/trajectory/"+str(v[0])+".csv' using 1:2 with lines lc " + str(cou) + " title '" + str(legend) +" fuel "+ str(v[0])+"',"
			else:
				s += "'"+  path + "data/trajectory/"+str(v[0])+".csv' using 1:2 with lines lc " + str(cou) + " notitle,"
		else:		
			s += "'"+  path + "data/trajectory/"+str(v[0])+".csv' using 1:2 with lines lc " + str(cou) + " title '" + str(round(v[1],2)) +"l fuel',"
		legendset[cou] = True

	print s[:-1]

elif TYPE == 'trajectoryFuleCost':

	#segment1 =  '50037'
	segment1 = "542931"
	segment2 = "424712"
	distance = 11.1
	res = con.query("select distinct a.tid , a.vehicleid from g_gps_can_data as a , g_gps_can_data as b where a.timestamp < b.timestamp and a.segmentkey = "+segment1+" and b.segmentkey = "+segment2+" and a.tid = b.tid order by a.vehicleid;").getresult()

	output = open(path +'data/trajectoryFuleCost.csv', 'wb')
	for i in res:
		low = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+" and segmentkey = "+segment1+") and tid = "+ str(i[0])+" ").getresult()
		high = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+" and timestamp > (select min(timestamp) from " + TABLE + " where tid = "+ str(i[0])+" and segmentkey = "+segment1+") and segmentkey = "+segment2+") and tid = "+ str(i[0])+" ").getresult()
		speed = con.query("select avg(speedMod) from " + TABLE + " where timestamp >= '" + low[0][1] + "' and timestamp <= '" + high[0][1] + "' and tid = "+ str(i[0])+" ").getresult()

		#print str(high[0][2] - low[0][2]) + " " + str(high[0][0] - low[0][0]) + " " + str(i[0]) 

		if (high[0][2] - low[0][2]) < 11.5:
			output.writelines(str(speed[0][0]) + " " + str((high[0][0] - low[0][0])/distance) + "\n")

	print "set output '" + path + "images/trajectoryFuleCost.png';"
	print "set ylabel 'Fuel efficiency (l/km)'"
	print "set xlabel 'Speed (km/h)'"
	print "f(x) = a*x**2 + b*x +c"
	print "fit f(x) '" + path + "data/trajectoryFuleCost.csv' using 1:2 via a,b,c"
	s = "plot "
	s += "'"+  path + "data/trajectoryFuleCost.csv'  notitle ,"
	print s + " f(x) lw 2 lc rgb 'black' title 'Regression line'"
	
elif TYPE == 'trajectoryCruise':

		#segment1 =  '50037' #"542931"
	segment1 = "542931"
	segment2 = "424712"

	res = con.query("select distinct a.tid , a.vehicleid from g_gps_can_data as a , g_gps_can_data as b where a.timestamp < b.timestamp and a.segmentkey = "+segment1+" and b.segmentkey = "+segment2+" and a.tid = b.tid order by a.vehicleid;").getresult()
	res = [[10392,1],[7167,1],[7312,1],[6915,1]]
	#res = [[7302,1],[6966,1]]
	toplot = []
	for i in res:

		low = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+" and segmentkey = "+segment1+") and tid = "+ str(i[0])+" ").getresult()

		#high = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp  = (select min + interval '71 second' from (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+" and segmentkey = "+segment1+") as foo) and tid = "+ str(i[0])+" ").getresult()
		#high = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp  = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+"  and kmcounter > "+ str(low[0][2] + 0.98) + ") and tid = "+ str(i[0])+" ").getresult()
		#print high
		high = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+" and timestamp > (select min(timestamp) from " + TABLE + " where tid = "+ str(i[0])+" and segmentkey = "+segment1+") and segmentkey = "+segment2+") and tid = "+ str(i[0])+" ").getresult()

		#res2 = con.query("select kmcounter, avg(speedMod) from " + TABLE + " where timestamp >= '" + low[0][1] + "' and timestamp <= '" + high[0][1] + "' and tid = "+ str(i[0])+" group by kmcounter order by kmcounter").getresult()

		res2 = con.query("select timestamp, speedMod from " + TABLE + " where timestamp >= '" + low[0][1] + "' and timestamp <= '" + high[0][1] + "' and tid = "+ str(i[0])+" order by timestamp").getresult()


		output = open(path +'data/trajectory/'+ str(i[0])+'.csv', 'wb')
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		
		if len(res2) > 0:
			begin = getTime(res2[0][0])
			#begin =res2[0][0]
			toplot.append([i[0], high[0][0] - low[0][0]])
			for r  in range(0,len(res2)):

				temp = str(getTime(res2[r][0]) - begin)
				#temp = res2[r][0] - begin
				res2[r] = list(res2[r])
				res2[r][0] = temp
				writer.writerow(res2[r])

	
	print "set output '" + path + "images/trajectoryCruise.png';"
	print "set ylabel 'speed(km/t)'"
	print "set xlabel 'time(s)'"
	#print "set xr[0:1.5]"
	s = "plot "
	for v in toplot:
		s += "'"+  path + "data/trajectory/"+str(v[0])+".csv' using 1:2 with lines title '"+str(v[0] ) + " " + str(v[1]) +"',"
	print s[:-1]

elif TYPE == 'trajectoryTrafficLight':

	if sys.argv[3] == "1":
		segment1 = "645539"
		segment2 = "71589"
	elif sys.argv[3] == "2":
		segment1 = "550218"
		segment2 = "550208"

	res = con.query("select distinct a.tid , a.vehicleid from g_gps_can_data as a , g_gps_can_data as b where a.timestamp < b.timestamp and a.segmentkey = "+segment1+" and b.segmentkey = "+segment2+" and a.tid = b.tid and a.timestamp::time > '9:00:00' and a.timestamp::time < '15:00:00' order by a.vehicleid;").getresult()

	toplot = []
	for i in res:

		low = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+" and segmentkey = "+segment1+") and tid = "+ str(i[0])+" ").getresult()

		high = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp  = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+"  and segmentkey = "+segment2+") and tid = "+ str(i[0])+" ").getresult()

		res2 = con.query("select timestamp, speedMod from " + TABLE + " where timestamp >= '" + low[0][1] + "' and timestamp <= '" + high[0][1] + "' and tid = "+ str(i[0])+" order by timestamp").getresult()


		output = open(path +'data/trajectory/'+ str(i[0])+'.csv', 'wb')
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		
		if len(res2) > 0:
			begin = getTime(res2[0][0])
			#begin =res2[0][0]
			stopped = False
			for r  in range(0,len(res2)):
				if(res2[r][1] == 0):
					stopped = True
				temp = str(getTime(res2[r][0]) - begin)
				#temp = res2[r][0] - begin
				res2[r] = list(res2[r])
				res2[r][0] = temp
				writer.writerow(res2[r])
			if getTime(high[0][1]) - getTime(low[0][1]) < 180:
				toplot.append([i[0], high[0][0] - low[0][0],float(high[0][2]) - float(low[0][2]),stopped,getTime(high[0][1]) - getTime(low[0][1])])
	
	avgstop = [0.0,0.0,0]
	avgrun = [0.0,0.0,0]
	for i in toplot:
		if i[3]:
			avgstop[0] += i[1]
			avgstop[1] += i[4]
			avgstop[2] += 1
		elif not i[3]:
			avgrun[0] += i[1]
			avgrun[1] += i[4]
			avgrun[2] += 1			

	#DO NOT DELETE
	#print "avg fuel stop " +str(avgstop[0]/avgstop[2])+ " avg run " +str(avgrun[0]/avgrun[2])+ ""
	#print "avg time stop " +str(avgstop[1]/avgstop[2])+ " avg run " +str(avgrun[1]/avgrun[2])+ ""
	print "set output '" + path + "images/trajectoryTrafficLight.png';"
	print "set ylabel 'Speed(km/t)'"
	print "set xlabel 'Time(s)'"
	
	if sys.argv[3] == "2":
		print "set xr[0:]"
	else:
		print "set xr[0:]"
	s = "plot "
	
	legendset = {}
	toplot.sort(key=lambda tup: tup[1])
	
	for v in toplot:
		#print "len " + str(v[2]) 
		cou = 0
		if v[1]< 0.01:
			cou = 3
			legend = "[0, 0.01) l"
		elif v[1] < 0.03:
			cou = 4
			legend = "[0.01, 0.03) l"
		elif v[1] < 0.05:
			cou = 2
			legend = "[0.03, 0.05) l"
		elif v[1] < 0.07:
			cou = 9
			legend = "[0.05, 0.07) l"
		elif v[1] <= 0.09:
			cou = 13
			legend = "[0.07, 0.09] l"

		#print cou
		if(not cou in legendset):
			s += "'"+  path + "data/trajectory/"+str(v[0])+".csv' using 1:2 with lines lc " + str(cou) + " title '" + str(legend) +"',"
		else:
			s += "'"+  path + "data/trajectory/"+str(v[0])+".csv' using 1:2 with lines lc " + str(cou) + " notitle,"

		legendset[cou] = True
	print s[:-1]
	


elif TYPE == 'idle2':
	q = "select round((idle_percentage*100)/5)*5 as idle,"
	for i in clusters:
		q += "count(case when km_pr_l <"+str(i[0])+" then 1 end)::float/count(*)*100,"
	q += "count(*) from " + TABLE + " group by idle order by idle;"
	res = con.query(q).getresult()
	
	output = open(path + 'data/idle2.csv', 'w+')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/idle2.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'Percent of trip in idle (%)'"
	print "set xtics 10"
	print "set yrange[0:100]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set logscale y2 10"
	print "set key opaque"
	
	s = "plot "	
	for i in range(len(clusters)+1, 1, -1):
		j= i-2
		s += "'" + path + "data/idle2.csv' using 1:" + str(i) + " w filledcurves x1 linestyle " + str(clusters[j][2]) + " title '" + str(clusters[j][1]) + "', "
	
	print s + "'" + path + "data/idle2.csv' using 1:" + str(len(clusters)+2) + " with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"
	
elif TYPE == 'idle3':
	q = "select * from (select round(idle_time::numeric/50,0)*50 as idle,"
	for i in clusters:
		q += "count(case when km_pr_l <"+str(i[0])+" then 1 end)::float/count(*)*100,"
	q += "count(*) from " + TABLE + " group by idle order by idle)a where idle>=250;"
	res = con.query(q).getresult()
	
	output = open(path + 'data/idle3.csv', 'w+')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/idle3.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'Idle time (s)'"
	print "set yrange[0:100]"
	print "set xrange[250:1500]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set key opaque"
	print "set xtics 100"

	s = "plot "	
	for i in range(len(clusters)+1, 1, -1):
		j= i-2
		s += "'" + path + "data/idle3.csv' using 1:" + str(i) + " w filledcurves x1 linestyle " + str(clusters[j][2]) + " title '" + str(clusters[j][1]) + "', "
	
	print s + "'" + path + "data/idle3.csv' using 1:" + str(len(clusters)+2) + " with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"
	
elif TYPE == 'normalRoad':
	q = "select round((PNormalRoad)::numeric,2),"
	for i in clusters:
		q += "count(case when km_pr_l <"+str(i[0])+" then 1 end)::float/count(*)*100,"
	q += "count(*) from " + TABLE + " where total_km >= 0.1 and PNormalRoad is not null  group by round order by round;"
	res = con.query(q).getresult()
	
	output = open(path + 'data/normalRoad.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/normalRoad.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'Driving on main roads (%)'"
	print "set yrange[0:100]"
	print "set xrange[0:1]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set key opaque"
	
	s = "plot "	
	for i in range(len(clusters)+1, 1, -1):
		j= i-2
		s += "'" + path + "data/normalRoad.csv' using 1:" + str(i) + " w filledcurves x1 linestyle " + str(clusters[j][2]) + " title '" + str(clusters[j][1]) + "', "
	print s + "'" + path + "data/normalRoad.csv' using 1:" + str(len(clusters)+2) + " with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"

elif TYPE == 'smallRoad':
	#res = con.query("select round((PSmallRoad)::numeric,2),count(case when km_pr_l <"+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l < "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " where total_km >= 0.1 and PSmallRoad is not null group by round order by round;").getresult()
	
	q = "select round((PSmallRoad)::numeric,2),"
	for i in clusters:
		q += "count(case when km_pr_l <"+str(i[0])+" then 1 end)::float/count(*)*100,"
	q += "count(*) from " + TABLE + " where total_km >= 0.1 and PSmallRoad is not null  group by round order by round;"
	res = con.query(q).getresult()
	
	output = open(path + 'data/smallRoad.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/smallRoad.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'Driving on small roads (%)'"
	print "set yrange[0:100]"
	print "set xrange[0:]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set key opaque"
	#print "plot '" + path + "data/smallRoad.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/smallRoad.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/smallRoad.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/smallRoad.csv' using 1:5 with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"
	
	s = "plot "	
	for i in range(len(clusters)+1, 1, -1):
		j= i-2
		s += "'" + path + "data/smallRoad.csv' using 1:" + str(i) + " w filledcurves x1 linestyle " + str(clusters[j][2]) + " title '" + str(clusters[j][1]) + "', "
	print s + "'" + path + "data/smallRoad.csv' using 1:" + str(len(clusters)+2) + " with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"

elif TYPE == 'moterRoad':
	#res = con.query("select round((pmoterroad)::numeric,2),count(case when km_pr_l <"+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l < "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " where total_km >= 0.1 and pmoterroad is not null group by round order by round;").getresult()
	
	q = "select round((pmoterroad)::numeric,2),"
	for i in clusters:
		q += "count(case when km_pr_l <"+str(i[0])+" then 1 end)::float/count(*)*100,"
	q += "count(*) from " + TABLE + " where total_km >= 0.1 and pmoterroad is not null  group by round order by round;"
	res = con.query(q).getresult()
	
	output = open(path + 'data/moterRoad.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/moterRoad.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'Driving on motorways (%)'"
	print "set yrange[0:100]"
	print "set xrange[0:0.1]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set key opaque"
	#print "plot '" + path + "data/moterRoad.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/moterRoad.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/moterRoad.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/moterRoad.csv' using 1:5 with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"
	s = "plot "	
	for i in range(len(clusters)+1, 1, -1):
		j= i-2
		s += "'" + path + "data/moterRoad.csv' using 1:" + str(i) + " w filledcurves x1 linestyle " + str(clusters[j][2]) + " title '" + str(clusters[j][1]) + "', "
	print s + "'" + path + "data/moterRoad.csv' using 1:" + str(len(clusters)+2) + " with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"
	

elif TYPE == 'testRoad':

	res = con.query("select moterroad, km_pr_l, vehicleid from "+TABLE+" where pmoterroad is not null order by vehicleid;").getresult()
	vehicles = []
	for r in range(0, len(res)-1):
		if r==0 or not res[r][2]==res[r-1][2]:
			output = open(path + 'data/'+str(res[r][2])+'testRoad.csv', 'w+')
			writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			vehicles.append(res[r][2])
		writer.writerow(res[r])
		
	print "set output '" + path + "images/testRoad.png';"
	print "set ylabel 'Fuel (km/l)';"
	print "set xlabel 'P normal Road '"
	
	s = "plot "
	for v in vehicles:
		s += "'" + path + "data/"+str(v) + "testRoad.csv' using 1:2 title '" + str(v) + "',"
	print s[:-1]


elif TYPE == 'cruiseCounter':
	print "set output '" + path + "images/cruiseCounter.png';"
	print "set ylabel 'Number of records with steady speed (x 10^3)"
	print "set xlabel 'Minimum length (s)'"
	print "set arrow from 20,0 to 20,849.889 lw 2 nohead"
	print "set arrow from 10,849.889 to 20,849.889 lw 2 nohead"
	
	print "plot '" + path + "data/cruiseCounter0.csv' using 1:($2/1000) with lines lw 3 title '+/- 0 km/h','" + path + "data/cruiseCounter1.csv' using 1:($2/1000) with lines lw 3 title '+/- 1 km/h','" + path + "data/cruiseCounter2.csv' using 1:($2/1000) with lines lw 3 title '+/- 2 km/h', '" + path + "data/cruiseCounter3.csv' using 1:($2/1000) with lines lw 3 title '+/- 3 km/h','" + path + "data/cruiseCounter4.csv' using 1:($2/1000) with lines lw 3 title '+/- 4 km/h'"

elif TYPE == 'cruisep':
	q = "select * from (select round((cruise_percentage)::numeric,2)*100 as round,"
	for i in clusters:
		q += "count(case when km_pr_l <"+str(i[0])+" then 1 end)::float/count(*)*100,"
	q += "count(*) as c from " + TABLE + " where total_km >= 0.1 group by round order by round)a where c > 10;"
	res = con.query(q).getresult()
	
	output = open(path + 'data/cruisep.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/cruisep.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'Steady speed (%) '"
	print "set yrange[0:100]"
	print "set xrange[0:]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set logscale y2 10 "
	print "set key opaque"
	print "set xtics 5"

	s = "plot "	
	for i in range(len(clusters)+1, 1, -1):
		j= i-2
		s += "'" + path + "data/cruisep.csv' using 1:" + str(i) + " w filledcurves x1 linestyle " + str(clusters[j][2]) + " title '" + str(clusters[j][1]) + "', "
	print s + "'" + path + "data/cruisep.csv' using 1:" + str(len(clusters)+2) + " with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"

elif TYPE == 'cruiseSpeedKml':
	vehicles = con.query("select distinct vehicleid from " + TABLE + " order by vehicleid;").getresult()
	allOutput = open(path + 'data/cruiseSpeedKml.csv', 'wb')
	allWriter = csv.writer(allOutput, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for v in vehicles:
		res = con.query("select  cruisespeed, case when length = 0 then 0 else fuel/length end from " + TABLE + " where cruisespeed>0 and cruisespeed<200 and vehicleid = " + str(v[0]) +" and time> 0;").getresult()
		output = open(path + 'data/'+str(v[0])+'cruiseSpeedKml.csv', 'wb')
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for r in res:
			writer.writerow(r)
			allWriter.writerow(r)
		
	print "set output '" + path + "images/cruiseSpeedKml.png';"
	print "set ylabel 'Fuel efficiency (l/km)'"
	print "set xlabel 'Cruise speed (km/h)'"
#	print "set xrange[0:150]"
	print "set yr [0:0.5]"
	print "set xtics 10"
	
	print "f(x) = a*x**2 + b*x + c"
	print "fit f(x) '" + path + "data/cruiseSpeedKml.csv' using 1:2 via a,b,c"
	
	s = "plot "
	for v in vehicles:
		#print patterns[v[0]][0] + "(x) = a" + str(v[0]) + "*x**2 + b"+str(v[0])+"*x + c"+str(v[0])
		#print "fit " + patterns[v[0]][0] + "(x) '" + path + "data/"+str(v[0]) + "cruiseSpeedKml.csv' using 1:2 via a"+str(v[0])+"," +"b" +str(v[0])+"," +"c" +str(v[0])
		s += "'"+  path + "data/"+str(v[0])+"cruiseSpeedKml.csv' title 'Vehicle " + str(v[0]) + "'lc rgb '"+ patterns[v[0]][1] +"',"
		#s+=patterns[v[0]][0] + "(x) notitle lc rgb '"+ patterns[v[0]][1] +"',"
	print s + " f(x) lw 2 lc rgb 'black' title 'Regression line'"

elif TYPE == 'cruiseSpeedKmlAvg':
	res = con.query("select cruisespeed, avg(case when length = 0 then 0 else fuel/length end) from " + TABLE + " group by cruiseSpeed;").getresult()
	output = open(path + 'data/cruiseSpeedKmlAvg.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)
		
	print "set output '" + path + "images/cruiseSpeedKmlAvg.png';"
	print "set ylabel 'Fuel efficiency (l/km)'"
	print "set xlabel 'Cruise speed (km/h)'"
#	print "set xrange[0:150]"
	print "set yr [0:0.5]"
	print "set xtics 10"
	
	print "f(x) = a*x**2 + b*x + c"
	print "fit f(x) '" + path + "data/cruiseSpeedKmlAvg.csv' using 1:2 via a,b,c"
	
	print "plot '"+  path + "data/cruiseSpeedKmlAvg.csv' notitle, f(x) lw 2 lc rgb 'black' title 'Regression line'"


elif TYPE == 'trafficlight':
	q = "select round((tlcounter)::numeric,1),"
	for i in clusters:
		q += "count(case when km_pr_l <"+str(i[0])+" then 1 end)::float/count(*)*100,"
	q += "count(*) from " + TABLE + " where total_km >= 0.1 group by round order by round;"
	res = con.query(q).getresult()
	
	output = open(path + 'data/trafficlight.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/trafficlight.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'traffic lights pr km '"
	print "set yrange[0:100]"
	print "set xrange[0:2.5]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set logscale y2 10 "
	print "set key opaque"

	s = "plot "	
	for i in range(len(clusters)+1, 1, -1):
		j= i-2
		s += "'" + path + "data/trafficlight.csv' using 1:" + str(i) + " w filledcurves x1 linestyle " + str(clusters[j][2]) + " title '" + str(clusters[j][1]) + "', "
	print s + "'" + path + "data/trafficlight.csv' using 1:" + str(len(clusters)+2) + " with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"

elif TYPE == 'trafficlightgreen':
	q = "select round((tlgreencounter)::numeric,1),"
	for i in clusters:
		q += "count(case when km_pr_l <"+str(i[0])+" then 1 end)::float/count(*)*100,"
	q += "count(*) from " + TABLE + " where total_km >= 0.1 group by round order by round;"
	res = con.query(q).getresult()
	
	output = open(path + 'data/trafficlightgreen.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/trafficlightgreen.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'traffic lights drive through pr km '"
	print "set yrange[0:100]"
	print "set xrange[0:2.5]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set logscale y2 10 "
	print "set key opaque"
	
	s = "plot "	
	for i in range(len(clusters)+1, 1, -1):
		j= i-2
		s += "'" + path + "data/trafficlightgreen.csv' using 1:" + str(i) + " w filledcurves x1 linestyle " + str(clusters[j][2]) + " title '" + str(clusters[j][1]) + "', "
	print s + "'" + path + "data/trafficlightgreen.csv' using 1:" + str(len(clusters)+2) + " with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"

elif TYPE == 'trafficlightred':
	q = "select round((tlredcounter)::numeric,1),"
	for i in clusters:
		q += "count(case when km_pr_l <"+str(i[0])+" then 1 end)::float/count(*)*100,"
	q += "count(*) from " + TABLE + " where total_km >= 0.1 group by round order by round;"
	res = con.query(q).getresult()
	
	output = open(path + 'data/trafficlightred.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/trafficlightred.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'traffic lights related stops pr km '"
	print "set yrange[0:100]"
	print "set xrange[0:]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set logscale y2 10 "
	print "set key opaque"

	s = "plot "	
	for i in range(len(clusters)+1, 1, -1):
		j= i-2
		s += "'" + path + "data/trafficlightred.csv' using 1:" + str(i) + " w filledcurves x1 linestyle " + str(clusters[j][2]) + " title '" + str(clusters[j][1]) + "', "
	print s + "'" + path + "data/trafficlightred.csv' using 1:" + str(len(clusters)+2) + " with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"

elif TYPE == 'trafficlightratio':
	q = "select round((tlredcounter/tlcounter)::numeric,1),"
	for i in clusters:
		q += "count(case when km_pr_l <"+str(i[0])+" then 1 end)::float/count(*)*100,"
	q += "count(*) from " + TABLE + " where total_km >= 0.1 and tlcounter > 0 group by round order by round;"
	res = con.query(q).getresult()
	
	output = open(path + 'data/trafficlightratio.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/trafficlightratio.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'percentage traffic lights related stops'"
	print "set yrange[0:100]"
	print "set xrange[0:]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	#print "set logscale y2 10 "
	print "set key opaque"
	
	s = "plot "	
	for i in range(len(clusters)+1, 1, -1):
		j= i-2
		s += "'" + path + "data/trafficlightratio.csv' using 1:" + str(i) + " w filledcurves x1 linestyle " + str(clusters[j][2]) + " title '" + str(clusters[j][1]) + "', "
	print s + "'" + path + "data/trafficlightratio.csv' using 1:" + str(len(clusters)+2) + " with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"


elif TYPE == 'idleDuration':
	output = open(path + 'data/idleDuration.csv', 'wb')
	for i in range(0,505, 5):
		res = con.query("select count(*) from " +TABLE + " where stopped > " + str(i) + ";").getresult()
		print >> output, str(i) + " " + str(res[0][0])

	print "set output '" + path + "images/idleDuration.png';"
	print "set ylabel 'Number of idle periods"
	print "set xlabel 'Minimum duration (s)'"
	print "set ytics 2500"
	print "set xtics 50"
	
	minDuration = '250'
	temp = con.query("select count(*) from " +TABLE + " where stopped > " + minDuration + ";").getresult()[0][0]
	
	print "set arrow from " + minDuration + ",0 to " + minDuration + "," + str(temp) + "lw 2 nohead"
	print "set arrow from 0," + str(temp) + " to " + minDuration + "," + str(temp) + " lw 2 nohead"
	print "plot '" + path + "data/idleDuration.csv' using 1:2 with lines lw 3 notitle"

elif TYPE == 'idleDuration2':
	print "set output '" + path + "images/idleDuration.png';"
	print "set ylabel 'Number of idle records (x 10^3)"
	print "set xlabel 'Minimum duration (s)'"
	print "set xtics 50"
	
	print "set arrow from 500,0 to 500,247.382 lw 2 nohead"
	print "set arrow from 0,247.382 to 500,247.382 lw 2 nohead"
	print "plot '" + path + "data/idleDuration.csv' using 1:($2/1000) with lines lw 3 notitle"

elif TYPE == 'tlRange':
	print "set output '" + path + "images/tlRange.png';"
	print "set ylabel '"
	print "set xlabel 'Radius from Traficlight (m)'"
	#print "set logscale y 10"
	print "set yrange[0.1:]"
	
	print "set arrow from 25,0.1 to 25,0.348146454461 lw 2 nohead"
	print "set arrow from 0.1,0.348146454461 to 25,0.348146454461 lw 2 nohead"
	print "plot '" + path + "data/TlCounter.csv' with lines lw 3 notitle"

	
elif TYPE == 'idleRange':
	res = con.query("select idle, count(*) from (select round(count(case when stopped=1 then 1 end)/10)*10 as idle from " + TABLE + " group by tid)a group by idle order by idle;").getresult()
	
	output = open(path + 'data/idleRange.csv', 'w+')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/idleRange.png';"
	print "set ylabel 'Number of records';"
	print "set xlabel 'Idle range (s)';"

	print "plot '"+ path + "data/idleRange.csv' with boxes"
	
elif TYPE == 'idleRange2' or TYPE == 'idleRange22':
	vehicles = con.query("select distinct vehicleid from " + TABLE + " order by vehicleid;").getresult()
	s = ""

	for v in vehicles:
		if(TYPE == 'idleRange2'):
			s = "select * from (select round(stopped/100)*100 as idle, sum(stopped),count(stopped) from "+ TABLE + " where vehicleid =" + str(v[0]) + " and stopped < 800 group by idle order by idle)a where count > 0;"
		else:
			s = "select * from (select round(stopped/100)*100 as idle, sum(stopped),count(stopped) from "+ TABLE + " where vehicleid =" + str(v[0]) + " and stopped >= 800 group by idle order by idle)a where count > 0;"
		res = con.query(s).getresult()
		if(TYPE == 'idleRange2'):
			output = open(path + 'data/'+str(v[0])+'idleRange2.csv', 'w+')
		else:
			output = open(path + 'data/'+str(v[0])+'idleRange22.csv', 'w+')
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for r in res:
			writer.writerow(r)

	boxwidth= 100.0/(len(vehicles)+1)
	if(TYPE == 'idleRange2'):
		print "set output '" + path + "images/idleRange2.png';"
		print "set xtics 100"
		print "set xrange[0:800]"

	else:
		print "set output '" + path + "images/idleRange22.png';"
		print "set xtics 200"
		print "set xrange[800:5600]"

	print "set ylabel 'Sum of seconds in idle (s)'"
	print "set xlabel 'Idle range (s)'"
	print "set style fill solid border -1"
	print "set boxwidth " + str(boxwidth)
	print "set xtic rotate by -45 scale 0"
	#print "set logscale y 10"
	
	offset = 0
	s = "plot "
	for v in vehicles:
		if(TYPE == 'idleRange2'):
			s += "'" + path + "data/"+str(v[0]) + "idleRange2.csv' using ($1+"+ str(offset+(boxwidth/2)) + "):2 with boxes lc rgb '" + patterns[v[0]][1]+ "' fs pattern " + patterns[v[0]][2] + " title '" + str(v[0]) + "' ,"
		else:
			s += "'" + path + "data/"+str(v[0]) + "idleRange22.csv' using ($1+"+ str(offset+(boxwidth/2)) + "):2 with boxes lc rgb '" + patterns[v[0]][1]+ "' fs pattern " + patterns[v[0]][2] + " title '" + str(v[0]) + "' ,"
		offset+=boxwidth
	print s[:-1]

elif TYPE == 'idleRange3':
	xstart = '250'
	res = con.query("select stopped, fuel, vehicleid from "+TABLE+" where stopped>=" + xstart +" order by vehicleid;").getresult()
	vehicles = []
	for r in range(0, len(res)-1):
		if r==0 or not res[r][2]==res[r-1][2]:
			output = open(path + 'data/'+str(res[r][2])+'idleRange3.csv', 'w+')
			writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			vehicles.append(res[r][2])
		writer.writerow(res[r])
		
	print "set output '" + path + "images/idleRange3.png';"
	print "set ylabel 'Fuel (l)';"
	print "set xlabel 'Idle seconds (s)'"
	print "set xrange[" + xstart + ":]"
	print "set key left"
	print "set xtics 250"
	print "set ytics 0.1"
	
	s = "plot "
	for v in vehicles:
		print patterns[v][0] + "(x) = a" + str(v) + "*x + b"+str(v)
		print "fit " + patterns[v][0] + "(x) '" + path + "data/"+str(v) + "idleRange3.csv' using 1:2 via a"+str(v)+"," +"b" +str(v)
		print "set arrow from 3600,0 to 3600,"+patterns[v][0]+"(3600) lw 1 nohead"
		print "set arrow from "+xstart+","+patterns[v][0]+"(3600) to 3600,"+patterns[v][0]+"(3600) lw 1 nohead"
		s += "'" + path + "data/"+str(v) + "idleRange3.csv' using 1:2 title '" + str(v) + "' lc rgb '"+ patterns[v][1] +"', " + patterns[v][0] + "(x) notitle lc rgb '"+ patterns[v][1] +"',"
	print s[:-1]
	
elif TYPE == 'rpmRanges':
	vehicles = con.query("select distinct vehicleid from " + TABLE + ";").getresult()
	for v in vehicles:
		res = con.query("select * from (select round(rpm/100)*100 as r, count(*)::float as c from "+ TABLE + " where vehicleid =" + str(v[0]) + " group by r order by r)a where c>50;").getresult()
	
		output = open(path + 'data/'+str(v[0])+'rpmRanges.csv', 'w+')
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for r in res:
			writer.writerow(r)
			
	boxwidth= 100.0/(len(vehicles)+1)
	print "set output '" + path + "images/rpmRanges.png';"
	print "set ylabel 'Number of records';"
	print "set xlabel 'Round per minut';"
	print "set style fill solid border -1"
	print "set boxwidth " + str(boxwidth)
	print "set xtic rotate by -45 scale 0"
	#print "set logscale y 10"
	print "set xr [600:]"
	print "set xtics 100"
	
	offset = 0
	s = "plot "
	for v in vehicles:
		s += "'" + path + "data/"+str(v[0]) + "rpmRanges.csv' using ($1+"+ str(offset) + "):2 with boxes lc rgb '" + patterns[v[0]][1]+ "' fs pattern " + patterns[v[0]][2] + " title '" + str(v[0]) + "',"
		offset+=boxwidth
	print s[:-1]	

elif TYPE=="rpmSpeed":
	vehicles = con.query("select vehicleid from " + TABLE + " where dirty = false group by vehicleid order by vehicleid;").getresult()
	counter =0
	for v in vehicles:
		res = con.query("select rpm from "+ TABLE + " where vehicleid =" + str(v[0]) + " and dirty = false and idle=1 and rpm<2000 order by timestamp;").getresult()
		output = open(path + 'data/'+str(v[0])+'rpmSpeed.csv', 'w+')
		for r in res:
			print >> output, str(counter) + " " + str(r[0])
			counter+=1
	
	print "set output '" + path + "images/rpmSpeed.png';"
	print "set ylabel 'RPM';"
	print "set xlabel '';"
	print "set ytics 100"
	
	s = "plot "
	for v in vehicles:
		s += "'" + path + "data/"+str(v[0]) + "rpmSpeed.csv' lc rgb '" + patterns[v[0]][1]+ "' title 'Vehicle" + str(v[0]) + "',"
	print s + " 900"

elif TYPE=="rpmAcceleration":
	vehicles = con.query("select vehicleid from " + TABLE + " where dirty = false group by vehicleid order by vehicleid;").getresult()
	for v in vehicles:
		res = con.query("select acceleration2, rpm from "+ TABLE + " where vehicleid =" + str(v[0]) + " and dirty = false and acceleration2<0 order by timestamp;").getresult()
		output = open(path + 'data/'+str(v[0])+'rpmAcceleration.csv', 'w+')
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for r in res:
			writer.writerow(r)
	
	print "set output '" + path + "images/rpmAcceleration.png';"
	print "set ylabel 'RPM';"
	print "set xlabel 'Acceleration';"
	print "set key left"
	
	s = "plot "
	for v in vehicles:
		s += "'" + path + "data/"+str(v[0]) + "rpmAcceleration.csv' lc rgb '" + patterns[v[0]][1]+ "' title 'Vehicle" + str(v[0]) + "',"
	print s + " 900 lw 3 lc rgb 'black'"

elif TYPE == 'accelerationRanges':

	vehicles = con.query("select vehicleid, count(*) from " + TABLE + " where dirty = false group by vehicleid order by vehicleid;").getresult()
	
	granularity = 0.25
	for v in vehicles:
		res = con.query("select * from (select round(acceleration3::decimal*4)/4 as acc, count(*)::float as c from "+ TABLE + " where vehicleid =" + str(v[0]) + " and cruise = false and dirty = false group by acc order by acc)a where (acc > 0);").getresult()
		output = open(path + 'data/'+str(v[0])+'accelerationRanges.csv', 'w+')
		for r in res:
			print >> output, str(r[0]) + " " + str(float(r[1])/float(v[1]))
			
	boxwidth= (float(granularity))/(len(vehicles)+1)
	print "set output '" + path + "images/accelerationRanges.png';"
	print "set ylabel 'Percent of records in range (%)'" #TODO: Rename
	print "set xlabel 'Acceleration (m/s^2)'"
	print "set style fill solid border -1"
	print "set boxwidth " + str(boxwidth)
	print "set xtic rotate by -45 scale 0"
	print "set xtics " + str(float(granularity))
	print "set xr [0.125:3.45]"
	
	offset = 0
	s = "plot "
	for v in vehicles: 
		s += "'" + path + "data/"+str(v[0]) + "accelerationRanges.csv' using ($1+"+ str(offset) + "):($2*100) with boxes lc rgb '" + patterns[v[0]][1]+ "' fs pattern " + patterns[v[0]][2] + "  title '" + str(v[0]) + "',"
		offset+=boxwidth
	print s[:-1]

elif TYPE == 'accelerationRanges2':

	vehicles = con.query("select vehicleid, count(*) from " + TABLE + " group by vehicleid order by vehicleid;").getresult()
	
	granularity = 0.125
	for v in vehicles:
		res = con.query("select * from (select round(avgAcceleration::decimal*8)/8 as acc, count(*)::float as c from "+ TABLE + " where time > 10 and vehicleid =" + str(v[0]) + " and dirty is false group by acc order by acc)a where (acc > 0);").getresult()
		output = open(path + 'data/'+str(v[0])+'accelerationRanges2.csv', 'w+')
		for r in res:
			print >> output, str(r[0]) + " " + str(float(r[1])/float(v[1]))
			
	boxwidth= (float(granularity))/(len(vehicles)+1)
	print "set output '" + path + "images/accelerationRanges2.png';"
	print "set ylabel 'Percent of periods in range (%)'" #TODO: Rename
	print "set xlabel 'Acceleration (m/s^2)'"
	print "set style fill solid border -1"
	print "set boxwidth " + str(boxwidth)
	print "set xtic rotate by -40 scale 0"
	print "set xtics " + str(float(granularity))
	print "set xr [:2]"
	
	offset = 0
	s = "plot "
	for v in vehicles: 
		s += "'" + path + "data/"+str(v[0]) + "accelerationRanges2.csv' using ($1+"+ str(offset) + "):($2*100) with boxes lc rgb '" + patterns[v[0]][1]+ "' fs pattern " + patterns[v[0]][2] + "  title '" + str(v[0]) + "',"
		offset+=boxwidth
	print s[:-1]

elif TYPE == 'accelerationRanges3a':
	res = con.query("select b.vehicleid, round((b.count::float/c.count*100)::numeric,2) from (select vehicleid, count(*) from (select vehicleid, round(acceleration/5)*5 as acc from " + TABLE + ")a where acc=0 group by vehicleid)b, (select vehicleid, count(*) from " + TABLE + " group by vehicleid)c where b.vehicleid=c.vehicleid;").getresult()
	output = open(path + 'images/accelerationRanges3a', 'w+')
	print >> output, """
	\\begin{table}
	\\centering
	\\begin{tabular}{|c|c|} \\hline
	Vehicle id & \\%\\\\\\hline
	"""
	for r in res:
		print >> output, str(r[0]) + " & " + str(r[1]) + "\\\\\\hline"
	print >> output, """
	\\end{tabular}
	\\caption{Number of records where 0$\geq$ acceleration< 5}
	\\label{tb:accelerationRanges3a}
	\\end{table}
	"""
	
	
elif TYPE == 'accelerationRanges3b':

	vehicles = con.query("select vehicleid, count(*) from " + TABLE + " where dirty = false group by vehicleid order by vehicleid;").getresult()
	
	granularity = 5
	for v in vehicles:
		res = con.query("select * from (select round(acceleration/" +str(granularity) + ")*" +str(granularity) + " as acc, count(*) as c from "+ TABLE + " where vehicleid =" + str(v[0]) + " and cruise = false and dirty is false group by acc order by acc)a where (acc > 0);").getresult()
		output = open(path + 'data/'+str(v[0])+'accelerationRanges3.csv', 'w+')
		for r in res:
			print >> output, str(r[0]) + " " + str(float(r[1])/float(v[1]))
			
	boxwidth= (float(granularity))/(len(vehicles)+1)
	print "set output '" + path + "images/accelerationRanges3b.png';"
	print "set ylabel 'Percent of records in range (%)'" #TODO: Rename
	print "set xlabel 'Acceleration (???)'"
	print "set style fill solid border -1"
	print "set boxwidth " + str(boxwidth)
	print "set xtic rotate by -45 scale 0"
	print "set xtics " + str(float(granularity))
#	print "set xr [0.125:3.45]"
	
	offset = 0
	s = "plot "
	for v in vehicles: 
		s += "'" + path + "data/"+str(v[0]) + "accelerationRanges3.csv' using ($1+"+ str(offset) + "):($2*100) with boxes lc rgb '" + patterns[v[0]][1]+ "' fs pattern " + patterns[v[0]][2] + "  title '" + str(v[0]) + "',"
		offset+=boxwidth
	print s[:-1]

elif TYPE == 'accelerationRanges4':

	vehicles = con.query("select vehicleid, count(*) from " + TABLE + " group by vehicleid order by vehicleid;").getresult()
	
	granularity = 5
	for v in vehicles:
		res = con.query("select round(acc/" +str(granularity) + ")*" +str(granularity) + " as a, avg(fuel/time) as c from "+ TABLE + " where time>10 and vehicleid =" + str(v[0]) + " group by a order by a;").getresult()
		output = open(path + 'data/'+str(v[0])+'accelerationRanges4.csv', 'w+')
		for r in res:
			print >> output, str(r[0]) + " " + str(r[1])#str(float(r[1])/float(v[1]))
			
	boxwidth= (float(granularity))/(len(vehicles)+1)
	print "set output '" + path + "images/accelerationRanges4.png';"
	print "set ylabel 'Fuel (l/s)'"
	print "set xlabel 'Acceleration (???)'"
	print "set style fill solid border -1"
	print "set boxwidth " + str(boxwidth)
	print "set xtic rotate by -45 scale 0"
	print "set xtics " + str(float(granularity))
#	print "set xr [0.125:3.45]"
	print "set key left"
	
	offset = 0
	s = "plot "
	for v in vehicles: 
		s += "'" + path + "data/"+str(v[0]) + "accelerationRanges4.csv' using ($1+"+ str(offset) + "):($2) with boxes lc rgb '" + patterns[v[0]][1]+ "' fs pattern " + patterns[v[0]][2] + "  title '" + str(v[0]) + "',"
		offset+=boxwidth
	print s[:-1]
	
elif TYPE == 'acceleration3D':
	accGranularity = 0.25
	speedGranularity = 10
	vehicles = con.query('select distinct vehicleid from g_accdata3 order by vehicleid').getresult()
	vehicles.insert(0,[0])
	vehicles.insert(0,[100])
	for v in vehicles:
		if v[0] == 100:
			res = con.query("select s, a, case when stddev_samp(f) is null then 0 else stddev_samp(f) end from (select vehicleid,round(startspeed/10*10) as s, round(avgAcceleration::decimal*4)/4 as a, avg((fuel*1000)/time) as f from g_accdata3 where avgAcceleration>0 and avgAcceleration<=2 and time>=3 group by s, a, vehicleid order by s, a)t group by s,a;").getresult()
		elif v[0] == 0: 
			res = con.query("select round(startspeed/10*10) as s, round(avgAcceleration::decimal*4)/4 as a, avg((fuel*1000)/time) as f from g_accdata3 where avgAcceleration>0 and avgAcceleration<=2 and time>=3 group by s, a order by s, a;").getresult()
		else:
			res = con.query("select round(startspeed/10*10) as s, round(avgAcceleration::decimal*4)/4 as a, avg(fuel*1000/time) as f from g_accdata3 where avgAcceleration>0 and avgAcceleration<=2 and vehicleid=" +str(v[0]) + " and time>=3 group by s, a order by s, a;").getresult()
		#res = [[0,0,2], [0,1,3.5], [1,0,1], [1,1,3]]
		output = open('data/' +str(v[0]) + 'acceleration3D.csv', 'w+')
		oldX = 0.0
		temp0 = ''
		temp1 = ''
		temp2 = ''
				
		for r in range(0, len(res)):
			if (not oldX==res[r][0]):
				print >> output, temp0 
				print >> output, temp1
				print >> output, temp2
				temp0 = ''
				temp1 = ''
				temp2 = ''
			oldX = res[r][0]
			temp0 += str(res[r][0]) + " " + str(float(res[r][1])) + " 0\n"
			temp0 += str(res[r][0]) + " " + str(float(res[r][1])) + " 0\n"
			temp0 += str(res[r][0]) + " " + str(float(res[r][1])+accGranularity) + " 0\n"

			temp1 += str(res[r][0]) + " " + str(float(res[r][1])) + " 0\n"
			temp1 += str(res[r][0]) + " " + str(float(res[r][1])) + " " + str(float(res[r][2])) + "\n"
			temp1 += str(res[r][0]) + " " + str(float(res[r][1])+accGranularity) + " " + str(float(res[r][2])) + "\n"

			temp2 += str(float(res[r][0])+float(speedGranularity)) + " " + str(float(res[r][1])) + " 0\n"
			temp2 += str(float(res[r][0])+float(speedGranularity)) + " " + str(float(res[r][1])) + " " + str(float(res[r][2])) + "\n"
			temp2 += str(float(res[r][0])+float(speedGranularity)) + " " + str(float(res[r][1])+accGranularity) + " " + str(float(res[r][2])) + "\n"
		print >> output, temp0
		print >> output, temp1
		print >> output, temp2
		
	
		print "set output 'images/" +str(v[0]) + "acceleration3D.png'"
		print "set hidden3d"
	#	print 'set palette defined (0 "green",0.025 "blue",0.05 "violet",0.025 "yellow",0.1 "red")'
		print "set xlabel 'Start speed km/t'"
		print "set ylabel 'Acceleration (m/s^2)'"
		print "set label 1 'Fuel (ml/s)' center rotate by 90 at graph 0, graph 0, graph 0.5 offset -7"
		
		if v[0]==100:
			print "set label 1 'Standard deviation (ml/s)' center rotate by 90 at graph 0, graph 0, graph 0.5 offset -7"
				
		else:
			print "set cbrange[0:10]"
			print "set label 1 'Fuel (ml/s)' center rotate by 90 at graph 0, graph 0, graph 0.5 offset -7"
		print "set zr[0:]"
		print "set yr[0:2]"
		print "set xr[0:] reverse"
		print "splot 'data/" +str(v[0]) + "acceleration3D.csv' with pm3d notitle"

elif TYPE == 'accelerationStddevAcc':
	temp = con.query("select avgAcceleration from " + TABLE + " where avgAcceleration > 0 order by avgAcceleration").getresult()
	highAcc = temp[len(temp)-(len(temp)/100*5)][0]

	vehicles = con.query("select vehicleid from " + TABLE + " group by vehicleid order by vehicleid;").getresult()
	granularity = 10
	for v in vehicles:
		res = con.query("select round(startspeed::decimal/10)*10 as speed, avg(avgAcceleration), stddev_samp(avgAcceleration) from "+ TABLE + " where vehicleid =" + str(v[0]) + " and avgAcceleration > 0  group by speed order by speed;").getresult()
		output = open(path + 'data/'+str(v[0])+'accelerationStddevAcc.csv', 'w+')
		for r in res:
			print >> output, str(r[0]) + " " + str(r[1]) + " " + str(r[2])
			
	boxwidth= (float(granularity))/(len(vehicles)+1)
	print "set output '" + path + "images/accelerationStddevAcc.png';"
	print "set ylabel 'Standard deviation on acceleration'" #TODO: Rename
	print "set xlabel 'Start speed (km/h)'"
	print "set style fill solid border -1"
	print "set boxwidth " + str(boxwidth)
	print "set xtic rotate by -45 scale 0"
	print "set xtics " + str(float(granularity))
	print "set xr [0:100]"
	
	offset = 0
	s = "plot "
	for v in vehicles: 
		s += "'" + path + "data/"+str(v[0]) + "accelerationStddevAcc.csv' using ($1+"+ str(offset) + "):2:3 with yerrorbars lc rgb '" + patterns[v[0]][1]+ "'  title '" + str(v[0]) + "',"
		offset+=boxwidth
	print s[:-1]



elif TYPE == 'accelerationSpeed':
	vehicles = con.query("select distinct vehicleid as v from " + TABLE + " order by v;").getresult()
#	vehicles = [[3]]
	for v in vehicles:
		output = open(path + 'data/'+ str(v[0]) + 'accelerationSpeed.csv', 'w+')
		res = con.query("select avgAcceleration as a, startspeed from " + TABLE + " where time>0 and (avgAcceleration>0) and acceleration>0 and vehicleid= "+ str(v[0]) + "order by starttime;").getresult()		
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for r in res:
			writer.writerow(r)
		
	print "set output '" + path + "images/accelerationSpeed.png';"
	print "set xlabel 'Start speed'"
	print "set ylabel 'Acceleration'"
	
	s = "plot "
	for v in vehicles:
		s += "'" + path + "data/"+ str(v[0]) + "accelerationSpeed.csv' using 2:1 lc rgb '" + patterns[v[0]][1]+ "' title 'Vehicle " + str(v[0]) + "',"
	print s[:-1]



elif TYPE == 'accelerationSpeedFuel':
	vehicles = con.query("select distinct vehicleid as v from " + TABLE + " order by v;").getresult()
	for v in vehicles:
		output = open(path + 'data/'+ str(v[0]) + 'accelerationSpeedFuel.csv', 'w+')
		res = con.query("select * from (select startSpeed, endSpeed, (|/ ((fuel)/3.14))*5 as fuel from " + TABLE + " where avgAcceleration>0 and km > 0  and vehicleid= "+ str(v[0]) + ")s where fuel > 0;").getresult()		
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for r in res:
			writer.writerow(r)
		
	print "set output '" + path + "images/accelerationSpeedFuel.png';"
	print "set ylabel 'End speed (km/h)'"
	print "set xlabel 'Start speed (km/h)'"
	
	s = "plot "
	for v in vehicles:
		s += "'" + path + "data/"+ str(v[0]) + "accelerationSpeedFuel.csv' using 1:2:3 with points lt 1 pt 7 ps variable lc rgb '" + patterns[v[0]][1]+ "' title 'Vehicle " + str(v[0]) + "',"
	print s[:-1]

elif TYPE == 'accelerationSpeedFuel2':
	vehicles = con.query("select distinct vehicleid as v from " + TABLE + " order by v;").getresult()
	for v in vehicles:
		output = open(path + 'data/'+ str(v[0]) + 'accelerationSpeedFuel2.csv', 'w+')
		res = con.query("select * from (select startSpeed, avgAcceleration, (|/ ((fuel/time)/3.14))*21 as fuel from " + TABLE + " where avgAcceleration>0 and km > 0  and time> 10 and vehicleid= "+ str(v[0]) + ")s where fuel > 0;").getresult()		
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for r in res:
			writer.writerow(r)
		
	print "set output '" + path + "images/accelerationSpeedFuel2.png';"
	print "set xlabel 'Start speed (km/h)'"
	print "set ylabel 'Acceleration (m/s^2)'"
	
	s = "plot "
	for v in vehicles:
		s += "'" + path + "data/"+ str(v[0]) + "accelerationSpeedFuel2.csv' using 1:2:3 with points lt 1 pt 7 ps variable lc rgb '" + patterns[v[0]][1]+ "' title 'Vehicle " + str(v[0]) + "',"
	print s[:-1]
	
	
elif TYPE == 'accelerationFuelStart':
	starts = con.query("select * from (select distinct round((endspeed-startspeed)/10)*10 as start from " +  TABLE + ")s where start>0 order by start;").getresult()
	s = "plot "
	for ss in starts:
		res = con.query("select startspeed, fuel/time from " + TABLE + " where round((endspeed-startspeed)/10)*10=" + str(ss[0]) + " and endspeed>startspeed order by endspeed;").getresult()
		output = open(path + 'data/'+ str(int(ss[0])) + 'accelerationFuelStart.csv', 'w+')
		for r in res:
			print >> output, str(r[0]) + " " + str(r[1])
		
		if len(res)> 3:
			n = str(int(ss[0]))
			print "f"+ n + "(x) = a"+ n + "*x + b"+ n
			print "fit f"+ n + "(x) '" + path + "data/"+ n + "accelerationFuelStart.csv' using 1:2 via a"+ n + ",b"+ n
#			s += "'" + path + "data/"+ str(int(ss[0])) + "accelerationFuelStart.csv' title 'Speed diff " + str(ss[0]) + "',"
			s+= "f"+ n + "(x) title 'Speed difference = " + n + "',"
	
	print "set output '" + path + "images/accelerationFuelStart.png';"
	print "set ylabel 'Fuel (l/s)'"
	print "set xlabel 'Start speed (km/h)'"
	print "set xrange[0:150]"
	print "set yrange[0:]"
	print "set key left"
	
	if not s == '':
		print s[:-1]
	
elif TYPE == "accelerationFuelCounter":
	output= open(path + 'data/accelerationFuelCounter.csv', 'wb')
	for i in range(0,31):
		res = con.query('select stddev_samp(avgAcceleration) from ' + TABLE + ' where time>' + str(i)).getresult()
		for r in res:
			print >> output, str(i) + " " + str(r[0])
	
	print "set output '" + path + "images/accelerationFuelCounter.png';"
	print "set ylabel 'Standard deviation of acceleration'"
	print "set xlabel 'Min lenght (s)'"
	print "set yr[0:]"
	
	temp = str(con.query('select stddev_samp(avgAcceleration) from ' + TABLE + ' where time>10').getresult()[0][0])
	print "set arrow from 10,0 to 10," +temp + " nohead"
	print "set arrow from 0," + temp + " to 10," +temp + " nohead"
	print "plot 'data/accelerationFuelCounter.csv' with lines notitle"

elif TYPE == "accelerationCounter":
	output= open(path + 'data/accelerationCounter.csv', 'wb')
	for i in range(0,31):
		#stddev_samp(((fuel*1000)/time))
		#count(*)
		res = con.query('select stddev_samp(((fuel*1000)/time)) from ' + TABLE + ' where time>' + str(i)).getresult()
		for r in res:
			print >> output, str(i) + " " + str(r[0])
	
	print "set output '" + path + "images/accelerationCounter.png';"
	print "set ylabel 'Standard deviation of ml/s'"
	print "set xlabel 'Min lenght (s)'"
	print "set yr[0:]"
	
	mint = '3'
	temp = str(con.query('select stddev_samp(((fuel*1000)/time)) from ' + TABLE + ' where time>' + mint).getresult()[0][0])
	print "set arrow from " + mint + ",0 to " + mint + "," +temp + " nohead"
	print "set arrow from 0," + temp + " to " + mint + "," +temp + " nohead"
	print "plot 'data/accelerationCounter.csv' with lines notitle"

		
elif TYPE == 'accelerationFuelStart2' or  TYPE == 'accelerationFuelStart2Data':
	minTime = '3'
	starts = con.query("select * from (select distinct round(startspeed/10)*10 as start from " +  TABLE + " where time>" + minTime + ")s where start>0 order by start;").getresult()
	s = "plot "
	color = 1
	for ss in starts:
		res = con.query("select avgAcceleration, (fuel*1000)/time::float from " + TABLE + " where round(startspeed/10)*10=" + str(ss[0]) + " and endspeed>startspeed and time>=" + minTime + " order by endspeed;").getresult()
		output = open(path + 'data/'+ str(int(ss[0])) + TYPE + '.csv', 'w+')
		
		for r in res:
			print >> output, str(r[0]) + " " + str(r[1])
		
		if len(res)> 3:
			n = str(int(ss[0]))
			print "f"+ n + "(x) = a"+ n + "*x + b"+ n
			print "fit f"+ n + "(x) '" + path + "data/"+ n + TYPE+ ".csv' using 1:2 via a"+ n + ",b"+ n
			if TYPE == 'accelerationFuelStart2Data':
				s += "'" + path + "data/"+ n + TYPE +".csv' lc " + str(color) + " notitle,"
#			if len(res)>100 or TYPE == 'accelerationFuelStart2Data':
			s+= "f"+ n + "(x) lc " + str(color) + " title 'Start speed: " + n + "(" + str(len(res)) + ")'," #sprintf('Start speed: %d (%2.1f)'," +n+", a"+ n + "),"
		color += 1
	
	print "set output '" + path + "images/" +TYPE + ".png';"
	print "set ylabel 'Fuel (ml/s)'"
	print "set xlabel 'Acceleration (m/s^2)'"
	print "set xrange[0:3]"
	print "set key outside opaque"
	
	if not s == '':
		print s[:-1]

elif TYPE == 'song' or  TYPE == 'songData':
	minTime = '10'
	starts = con.query("select * from (select distinct round(startspeed/10)*10 as start from " +  TABLE + " where time>" + minTime + ")s where start>0 and start<90 order by start;").getresult()
	s = "plot "
	color = 1
	for ss in starts:
		n = str(int(ss[0]))
		print "f"+ n + "(x) = a"+ n + "*x + b"+ n
		print "fit f"+ n + "(x) '" + path + "data/"+ n + ".0song.csv' using 1:3 via a"+ n + ",b"+ n
		if TYPE == 'songData':
			s += "'" + path + "data/"+ n + ".0song.csv' using 1:3 lc " + str(color) + " notitle,"
		s+= "f"+ n + "(x) lc " + str(color) + " title sprintf('Start speed: %d (%2.1f)'," +n+", a"+ n + ")," #'Start speed: " + n + "'
		color += 1
	
	print "set output '" + path + "images/"+ TYPE + ".png';"
	print "set ylabel 'Fuel by Song'"
	print "set xlabel 'Acceleration (m/s^2)'"
	print "set xrange[0:3]"
	print "set key outside opaque"
	
	if not s == '':
		print s[:-1]

elif TYPE == 'accelerationSpeedFuelTime':
	vehicles = con.query("select distinct vehicleid as v from " + TABLE + " order by v;").getresult()
	for v in vehicles:
		output = open(path + 'data/'+ str(v[0]) + 'accelerationSpeedFuelTime.csv', 'w+')
		res = con.query("select  time, endspeed-startspeed,(|/ ((fuel)/3.14))*4 as fuel from " + TABLE + " where avgAcceleration>0 and avgAcceleration <6 and km > 0 and vehicleid= "+ str(v[0]) + ";").getresult()		
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for r in res:
			writer.writerow(r)
		
	print "set output '" + path + "images/accelerationSpeedFuelTime.png';"
	print "set xlabel 'Time (s)'"
	print "set ylabel 'Speed difference (km/h)'"
	
	s = "plot "
	for v in vehicles:
		s += "'" + path + "data/"+ str(v[0]) + "accelerationSpeedFuelTime.csv' using 1:2:3 with points lt 1 pt 7 ps variable lc rgb '" + patterns[v[0]][1]+ "' title 'Vehicle " + str(v[0]) + "',"
	print s[:-1]

elif TYPE == 'accelerationFuel':
	res = con.query("select round(fuel::decimal*100, 0)/100 as f, count(*) from " + TABLE + " group by f order by f;").getresult()
	output = open(path + 'data/accelerationFuel.csv', 'w+')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)
		
	print "set output '" + path + "images/accelerationFuel.png';"
	print "set ylabel '"
	print "set xlabel ''"
#	print "set logscale y 10"
	print "set xrange[0:0.5]"
#	print "set arrow from 5, 0 to 5, 200000"
	print "plot '" + path + "data/accelerationFuel.csv' with lines"
	
elif TYPE == 'accelerationFuel2':
	vehicles = con.query("select distinct vehicleid as v from " + TABLE + " order by v;").getresult()
#	vehicles = [[3]]
	for v in vehicles:
		output = open(path + 'data/'+ str(v[0]) + 'accelerationFuel2.csv', 'w+')
#		res = con.query("select avgAcceleration, fuel from " + TABLE + " where acceleration>0 and km>0 and (extract(epoch from endtime)-extract(epoch from starttime) )>10 and vehicleid= "+ str(v[0]) + ";").getresult()
#		res = con.query("select avgAcceleration, fuel/km from " + TABLE + " where acceleration>0 and km>0 and (extract(epoch from endtime)-extract(epoch from starttime) )>10 and vehicleid= "+ str(v[0]) + ";").getresult()
		res = con.query("select avgAcceleration, fuel/time from " + TABLE + " where acceleration>0 and km>0 and time>10 and vehicleid= "+ str(v[0]) + ";").getresult()	
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for r in res:
			writer.writerow(r)
		
	print "set output '" + path + "images/accelerationFuel2.png';"
	print "set ylabel 'Fuel'"
	print "set xlabel 'Acceleration'"
	
	s = "plot "
	for v in vehicles:
		s += "'" + path + "data/"+ str(v[0]) + "accelerationFuel2.csv' lc rgb '" + patterns[v[0]][1]+ "' title 'Vehicle " + str(v[0]) + "',"
	print s[:-1]

elif TYPE == 'testSpeed':
	print "set output '" + path + "images/testSpeed.png';"
	print "set ylabel 'Number of records"
	print "set xlabel 'Speed Difference'"
	print "set xtics 5"
	print "plot '" + path + "data/testSpeed.csv' with lines lw 3 notitle"

elif TYPE == 'testClusters':
	print "set output '" + path + "images/testClusters.png';"
	print "set ylabel 'Percentage correctly classified"
	print "set xlabel 'Number of clusters'"
	print "plot '" + path + "data/classData.csv' with lines lw 3 notitle"
	
elif TYPE == 'steadySpeedExample':
	print "set output '" + path + "images/steadySpeedExample.png';"
	print "set ylabel 'Speed (km/h)"
	print "set xlabel 'Time (s)'"
	print "set yrange[30:55]"
	print "set xrange[0:62]"
	print "set ytics 2"
	
	print "set arrow from 4,50 to 39,50 lw 1 nohead"
	print "set arrow from 4,47 to 39,47 lw 4 nohead"
	print "set arrow from 4,53 to 39,53 lw 4 nohead"
	print "set arrow from 4,47 to 4,53 lw 4 nohead"
	print "set arrow from 39,47 to 39,53 lw 4 nohead"
	
	print "set arrow from 41,53 to 62,53 lw 1 nohead"
	print "set arrow from 41,50 to 62,50 lw 4 nohead"
	print "set arrow from 41,56 to 62,56 lw 4 nohead"
	print "set arrow from 41,50 to 41,56 lw 4 nohead"
	print "set arrow from 62,50 to 62,56 lw 4 nohead"
	print "plot '" + path + "data/steadySpeedExample' with lines lw 2 notitle"

elif TYPE == 'speedlimitCount':
	vehicles = con.query("select vehicleid as v, count(*) from " + TABLE + " group by v order by v;").getresult()
	for v in vehicles:
		output = open(path + 'data/'+ str(v[0]) + 'speedlimitCount.csv', 'w+')
		res = con.query("select round(d/5)*5 as r, count(*) from (select *, speedmod-speedlimit as d from (select case when g.direction='FORWARD' then speedlimit_forward else speedlimit_backward end as speedlimit,speedmod from osm_dk_20130501 as m, " + TABLE + " as g where m.segmentkey=g.segmentkey and dirty is false and vehicleid=" + str(v[0]) + ")s)t where d> 0 group by r order by r desc;").getresult()	
		for r in res:
			print >> output, str(r[0]) + " " + str(float(r[1])/v[1]*100)
	
			
	boxwidth= 5.0/(len(vehicles)+1)
	print "set output '" + path + "images/speedlimitCount.png';"
	print "set ylabel 'Number of records (%)'"
	print "set xlabel 'Faster than the speedlimit (km/h)';"
	print "set style fill solid border -1"
	print "set boxwidth " + str(boxwidth)
	print "set xtic rotate by -45 scale 0"
	#print "set logscale y 10"
	print "set xr [0:]"
	print "set xtics 5"
	
	offset = 0
	s = "plot "
	for v in vehicles:
		s += "'" + path + "data/"+str(v[0]) + "speedlimitCount.csv' using ($1+"+ str(offset+boxwidth/2) + "):2 with boxes lc rgb '" + patterns[v[0]][1]+ "' fs pattern " + patterns[v[0]][2] + " title '" + str(v[0]) + "',"
		offset+=boxwidth
	print s[:-1]
	
elif TYPE == "compareVehicles":
	res = con.query("""
		select a.vehicleid, acc::float/c as a, steady::float/c as s, dec::float/c as d, stopped::float/c as st, idle::float/c as i, o::float/c as o from 
			(select 
				vehicleid, 
				count(case when acceleration3<0 and cruise is false then 1 end) as dec, 
				count(case when cruise is true then 1 end) as steady, 
				count(case when acceleration3>0 and cruise is false then 1 end) as acc, 
				count(case when stopped=1 and idle=0 then 1 end) as stopped, 
				count(case when idle=1 then 1 end) as idle, 
				count(case when acceleration3=0 and cruise is false and stopped =0 then 1 end) as o 
			from g_gps_can_data where dirty is false group by vehicleid)a,
			(select 
				vehicleid,
				count(*) as c 
		from g_gps_can_data where dirty is false group by vehicleid)t 
		where a.vehicleid=t.vehicleid;""").getresult()
	
	for r in res:
		output = open(path + 'data/' + str(r[0]) + 'Compare.csv', 'wb')
		print >> output, 'Acceleration ' + str(r[1]) 
		print >> output, 'SteadySpeed ' + str(r[2])
		print >> output, 'Deceleration ' + str(r[3])
		print >> output, 'Stopped ' + str(r[4])
		print >> output, 'Idle ' + str(r[5])
		print >> output, 'Other ' + str(r[6])
		output.close()
#		print "python piechart.py data/" + str(r[0]) + "Compare.csv images/" + str(r[0]) + "Compare.png"
		os.system("python piechart.py data/" + str(r[0]) + "Compare.csv images/" + str(r[0]) + "Compare.png")

elif TYPE == 'compareVehicles2':
	"""set nokey
set polar
set angles degrees
npoints = 5
a1 = 360/npoints*1
a2= 360/npoints*2
a3= 360/npoints*3
a4= 360/npoints*4
a5= 360/npoints*5
set grid polar 360.
set size square
set style data lines
unset border
set arrow nohead from 0,0 to first 1*cos(a1) , 1*sin(a1)
set arrow nohead from 0,0 to first 1*cos(a2) , 1*sin(a2)
set arrow nohead from 0,0 to first 1*cos(a3) , 1*sin(a3)
set arrow nohead from 0,0 to first 1*cos(a4) , 1*sin(a4)
set arrow nohead from 0,0 to first 1*cos(a5) , 1*sin(a5)
a1_max = 10
a2_max = 5
a3_max = 100
a4_max = 2020
a5_max = 1
a1_min = 0
a2_min = 0
a3_min = 50
a4_min = 1980
a5_min = 0
set label "(0:10)" at cos(a1),sin(a1) center offset char 1,1
set label "(0:5)" at cos(a2),sin(a2) center offset char -1,1
set label "(50:100)" at cos(a3),sin(a3) center offset char -1,-1
set label "(1980:2020)" at cos(a4),sin(a4) center offset char 0,-1
set label "(0:1)" at cos(a5),sin(a5) center offset char 3,0
set xrange [-1:1]
set yrange [-1:1]
unset xtics
unset ytics
set rrange [0:1]
set rtics (""0,""0.25,""0.5,""0.75,""1)

plot 'data/spider.csv' using ($1==1?a1:($1==2?a2:($1==3?a3:($1==4?a4:($1==5?a5:$1))))):($1==1?(($2-a1_min)/(a1_max-a1_min)):($1==2?(($2-a2_min)/(a2_max-a2_min)):($1==3?(($2-a3_min)/(a3_max-a3_min)):($1==4?(($2-a4_min)/(a4_max-a4_min)):($1==5?(($2-a5_min)/(a5_max-a5_min)):$1))))) w l
pause -1"""


elif TYPE == 'accelerationTEST':
	res = con.query('select speedmod, rpm, acceleration from ' + TABLE + " where tid=9999 order by timestamp;").getresult()
	output = open(path + 'data/accelerationTEST.csv', 'wb+')
	counter = 0
	for r in res:
		print >> output, str(counter) + " " + str(r[0]) + " " + str(r[1]) + " " + str(r[2])
		counter += 1
	
	print "set output '" + path + "images/accelerationTEST.png';"
	print "set xlabel 'Time (s)'"
	print "set y2tics"

	print "plot '" + path + "data/accelerationTEST.csv' using 1:4 with lines title 'Acceleration', '" + path + "data/accelerationTEST.csv' using 1:3 with lines title 'RPM' axes x1y2"


elif TYPE == 'checkFuel':
	tids = con.query('select distinct tid from ' + TABLE).getresult()
	output = open(path + 'data/checkFuel.csv', 'wb+')
	counter = {}
#	tids= [['2930']]
	for t in tids:
		res = con.query('select timestamp, totalconsumed from ' + TABLE + " where tid=" +str(t[0]) + " order by timestamp;").getresult()
		for r in range(1,len(res)-1):
			temp= int(((res[r][1]-res[r-1][1])*1000)/(getTime(res[r][0])-getTime(res[r-1][0])))
			if temp in counter:
				counter[temp] += 1
			else:
				counter[temp] = 1
	for k, v in counter.items():
		print >> output,  str(k) + " " + str(v)
	
	print "set output '" + path + "images/checkFuel.png';"
	print "set boxwidth 1"
	print "set logscale y 10"
	print "set xtics 20"
	print "set xlabel 'Fuel (ml/s)'"
	print "set ylabel 'Number of records'"
	print "set xr [-180:180]"
	
	print "plot '" + path + "data/checkFuel.csv' with boxes notitle"

elif TYPE == 'idleTime':
	#TODO: Do not work
	val = 'idle_time, km_pr_l as val, |/ (total_fuel/3.14)'
	res = con.query("select " + val + " from " + TABLE + " where km_pr_l < 4  order by val;").getresult()
	output = open(path + 'data/' + TYPE + '_low_data.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	res = con.query("select " + val + " from " + TABLE + " where km_pr_l >= 4 and km_pr_l < 8 order by val;").getresult()
	output = open(path + 'data/' + TYPE + '_medium_data.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	res = con.query("select " + val + " from " + TABLE + " where km_pr_l > 8 order by val;").getresult()
	output = open(path + 'data/' + TYPE + '_high_data.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/idleTime.png';"
	print "set ylabel 'km/l';"
	print "set xlabel 'Idle time (s)';"

	s = "plot "
	s+= "'" + path + "data/" + TYPE + "_high_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"green\" title 'High' , "
	s+= "'" + path + "data/" + TYPE + "_medium_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"blue\" title 'Medium', "
	s+= "'" + path + "data/" + TYPE + "_low_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"red\" title 'Low'"
	print s

	
elif TYPE == 'idlePercent':
	#TODO: Do not work
	val = 'idle_percentage*100, km_pr_l as val, |/ (total_fuel/3.14)'
	res = con.query("select " + val + " from " + TABLE + " where km_pr_l < 4  order by val;").getresult()
	output = open(path + 'images/' + TYPE + '_low_data.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	res = con.query("select " + val + " from " + TABLE + " where km_pr_l >= 4 and km_pr_l < 8 order by val;").getresult()
	output = open(path + 'images/' + TYPE + '_medium_data.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	res = con.query("select " + val + " from " + TABLE + " where km_pr_l > 8 order by val;").getresult()
	output = open(path + 'images/' + TYPE + '_high_data.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/idlePercent.png';"
	print "set ylabel 'km/l';"
	print "set xlabel 'Percent of trip in idle (%)'"

	s = "plot "
	s+= "'" + path + "images/" + TYPE + "_high_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"green\" title 'High' , "
	s+= "'" + path + "images/" + TYPE + "_medium_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"blue\" title 'Medium', "
	s+= "'" + path + "images/" + TYPE + "_low_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"red\" title 'Low'"
	print s

else:
	print "Nothing"

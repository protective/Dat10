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

print "set terminal png size 1000,500;"


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

elif TYPE == 'trajectory':

	#segment1 =  '50037' #"542931"
	segment1 = "542931"
	segment2 = "424712"

	res = con.query("select distinct a.tid , a.vehicleid from g_gps_can_data as a , g_gps_can_data as b where a.timestamp < b.timestamp and a.segmentkey = "+segment1+" and b.segmentkey = "+segment2+" and a.tid = b.tid order by a.vehicleid;").getresult()
	res = [[6915,1],[7312,1],[10392,1]]
	#res = [[7302,1],[6966,1]]
	toplot = []
	for i in res:

		low = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+" and segmentkey = "+segment1+") and tid = "+ str(i[0])+" ").getresult()

		#high = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp  = (select min + interval '71 second' from (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+" and segmentkey = "+segment1+") as foo) and tid = "+ str(i[0])+" ").getresult()
		high = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp  = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+"  and kmcounter > "+ str(low[0][2] + 0.98) + ") and tid = "+ str(i[0])+" ").getresult()
		#print high
		#high = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+" and timestamp > (select min(timestamp) from " + TABLE + " where tid = "+ str(i[0])+" and segmentkey = "+segment1+") and segmentkey = "+segment2+") and tid = "+ str(i[0])+" ").getresult()

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

	
	print "set output '" + path + "images/trajectory.png';"
	print "set ylabel 'Speed(km/t)'"
	print "set xlabel 'Time(s)'"
	print "set xr[0:]"
	s = "plot "
	for v in toplot:
		s += "'"+  path + "data/trajectory/"+str(v[0])+".csv' using 1:2 with lines title '" + str(v[1]) +" l fuel',"
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

	#segment1 = "645538"
	#segment2 = "71591"

	segment1 = "645539"
	segment2 = "71589"

	res = con.query("select distinct a.tid , a.vehicleid from g_gps_can_data as a , g_gps_can_data as b where a.timestamp < b.timestamp and a.segmentkey = "+segment1+" and b.segmentkey = "+segment2+" and a.tid = b.tid and a.timestamp::time > '9:00:00' and a.timestamp::time < '15:00:00' order by a.vehicleid;").getresult()
	#res = [[6915,1],[7312,1],[10392,1]]
	#res = [[7302,1],[6966,1]]
	toplot = []
	for i in res:

		low = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+" and segmentkey = "+segment1+") and tid = "+ str(i[0])+" ").getresult()

		high = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp  = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+"  and segmentkey = "+segment2+") and tid = "+ str(i[0])+" ").getresult()
		#print high
		#high = con.query("select totalconsumed,timestamp,kmcounter from " + TABLE + " where timestamp = (select min(timestamp) from g_gps_can_data where tid = "+ str(i[0])+" and timestamp > (select min(timestamp) from " + TABLE + " where tid = "+ str(i[0])+" and segmentkey = "+segment1+") and segmentkey = "+segment2+") and tid = "+ str(i[0])+" ").getresult()

		#res2 = con.query("select kmcounter, avg(speedMod) from " + TABLE + " where timestamp >= '" + low[0][1] + "' and timestamp <= '" + high[0][1] + "' and tid = "+ str(i[0])+" group by kmcounter order by kmcounter").getresult()

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
			toplot.append([i[0], high[0][0] - low[0][0],float(high[0][2]) - float(low[0][2]),stopped])
	
	avgstop = [0.0,0]
	avgrun = [0.0,0]
	for i in toplot:
		if i[3]:
			avgstop[0] += i[1]
			avgstop[1] += 1
		elif not i[3]:
			avgrun[0] += i[1]
			avgrun[1] += 1			

	#print "avg stop " +str(avgstop[0]/avgstop[1])+ " avg run " +str(avgrun[0]/avgrun[1])+ ""

	print "set output '" + path + "images/trajectoryTrafficLight.png';"
	print "set ylabel 'Speed(km/t)'"
	print "set xlabel 'Time(s)'"
	print "set xr[0:]"
	s = "plot "
	
	legendset = {}
	toplot.sort(key=lambda tup: tup[1])
	
	for v in toplot:
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
	print "set xlabel 'Normal Road P'"
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
	print "set xlabel 'Small Road P'"
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
	print "set xlabel 'Motor Road P'"
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
		res = con.query("select * from (select round(acceleration3::decimal*4, 0)/4 as acc, count(*)::float as c from "+ TABLE + " where vehicleid =" + str(v[0]) + " and cruise = false and dirty = false group by acc order by acc)a where (acc > 0.1 or acc < -0.1)  and c > 800;").getresult()
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
	
	offset = 0
	s = "plot "
	for v in vehicles: 
		s += "'" + path + "data/"+str(v[0]) + "accelerationRanges.csv' using ($1+"+ str(offset) + "):($2*100) with boxes lc rgb '" + patterns[v[0]][1]+ "' fs pattern " + patterns[v[0]][2] + "  title '" + str(v[0]) + "',"
		offset+=boxwidth
	print s[:-1]

elif TYPE == 'accelerationFast':
	vehicles = con.query("select distinct vehicleid from " + TABLE + " order by vehicleid;").getresult()
	i = 0
	for v in vehicles:
		vid = str(v[0])
		res = con.query("select acceleration2 as acc from "+ TABLE + " where vehicleid =" + vid + " and dirty = false order by tid, timestamp;").getresult()
		output = open(path + 'data/'+str(v[0])+'accelerationFast.csv', 'w+')
		for r in res:
			print>> output, str(i) + " " + str(r[0])
			i+=1


	print "set output '" + path + "images/accelerationFast.png';"
	print "set ylabel 'Acceleration (m/s^2)'"
	print "set ytics 10"
	#print "set yrange[:10]"
	
	s = "plot "
	for v in vehicles: 
		s += "'" + path + "data/"+str(v[0]) + "accelerationFast.csv' lc rgb '" + patterns[v[0]][1]+ "'  title '" + str(v[0]) + "',"
	print s + " 0 lw 2 lc rgb 'black' notitle"

elif TYPE == 'acceleration2':
	output = open(path + 'data/acceleration2.csv', 'w+')
	for i in range(0, 35, 1):
		res = con.query("select count(case when acceleration > 0 and abs(EXTRACT(EPOCH FROM endtime)-EXTRACT(EPOCH FROM starttime))>" + str(i) + " then 1 end) as acc, count(case when acceleration< 0  and abs(EXTRACT(EPOCH FROM endtime)-EXTRACT(EPOCH FROM starttime))>" + str(i) + " then 1 end) as dec from " + TABLE + ";").getresult()		
		print>> output, str(i) + " " + str(res[0][0]) + " " + str(res[0][1])
		
	print "set output '" + path + "images/acceleration2.png';"
	print "set ylabel '"
	print "set xlabel ''"
	print "set arrow from 5, 0 to 5, 200000"
	print "plot '" + path + "data/acceleration2.csv' using 1:2 with lines lw 3 title 'Acceleration', '" + path + "data/acceleration2.csv' using 1:3 with lines lw 3 title 'Deceleration'"

elif TYPE == 'acceleration3':
	output = open(path + 'data/acceleration3.csv', 'w+')
	for i in range(0, 100, 1):
		res = con.query("select count(case when acceleration > 0 and abs(endspeed-startspeed)>" + str(i) + " then 1 end) as acc, count(case when acceleration< 0  and abs(endspeed-startspeed)>" + str(i) + " then 1 end) as dec from " + TABLE + ";").getresult()		
		print>> output, str(i) + " " + str(res[0][0]) + " " + str(res[0][1])
		
	print "set output '" + path + "images/acceleration3.png';"
	print "set ylabel '"
	print "set xlabel ''"
	print "set arrow from 5, 0 to 5, 200000"
	print "plot '" + path + "data/acceleration3.csv' using 1:2 with lines lw 3 title 'Acceleration', '" + path + "data/acceleration3.csv' using 1:3 with lines lw 3 title 'Deceleration'"
	
elif TYPE == 'acceleration4':
	output = open(path + 'data/acceleration4.csv', 'w+')
	for i in range(0, 100, 1):
		j = float(i)/1000
		res = con.query("select count(case when acceleration > 0 and fuel>" + str(j) + " then 1 end) as acc, count(case when acceleration< 0 and fuel>" + str(j) + " then 1 end) as dec from " + TABLE + ";").getresult()		
		print>> output, str(j) + " " + str(res[0][0]) + " " + str(res[0][1])
		
	print "set output '" + path + "images/acceleration4.png';"
	print "set ylabel '"
	print "set xlabel 'Fuel (ml)'"
	print "set style fill solid border -1"
	print "set boxwidth 1"
#	print "set xtics 0.002"
	print "set xtic rotate by -20 scale 0"
#	print "set arrow from 0.011, 0 to 0.011, 160000 lw 3 nohead"
	print "plot '" + path + "data/acceleration4.csv' using (($1*1000)+0.5):2 with boxes title 'Acceleration', '" + path + "data/acceleration4.csv' using (($1*1000)+0.5):3 with boxes title 'Deceleration'"

elif TYPE == 'acceleration5':
	vehicles = con.query("select distinct vehicleid from " + TABLE + ";").getresult()
	for v in vehicles:
		output = open(path + 'data/'+ str(v[0]) + 'acceleration5.csv', 'w+')
		res = con.query("select round(acceleration::decimal*20, 0)/20 as a, count(*) from g_accdata2 where fuel>0.001 and (acceleration>0) and vehicleid= "+ str(v[0]) + "group by a order by a desc;").getresult()		
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for r in res:
			writer.writerow(r)
		
	print "set output '" + path + "images/acceleration5.png';"
	print "set ylabel '"
	print "set xlabel ''"
	print "set xrange[0:10]"
	boxwidth= 0.1/(len(vehicles)+1)
	print "set boxwidth " + str(boxwidth)
	print "set style fill solid border -1"
	s = "plot "
	offset = 0
	for v in vehicles:
		s += "'" + path + "data/"+ str(v[0]) + "acceleration5.csv' using ($1+"+str(offset)+"):2 with boxes title 'Vehicle " + str(v[0]) + "',"
		offset += boxwidth
	print s[:-1]
	
elif TYPE == 'accelerationSpeed':
	vehicles = con.query("select distinct vehicleid as v from " + TABLE + " order by v;").getresult()
#	vehicles = [[3]]
	for v in vehicles:
		output = open(path + 'data/'+ str(v[0]) + 'accelerationSpeed.csv', 'w+')
		res = con.query("select avgAcceleration as a, startspeed from " + TABLE + " where (avgAcceleration>0) and acceleration>0 and vehicleid= "+ str(v[0]) + "order by starttime;").getresult()		
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
#	vehicles = [[3]]
	for v in vehicles:
		output = open(path + 'data/'+ str(v[0]) + 'accelerationSpeedFuel.csv', 'w+')
		res = con.query("select * from (select startSpeed, endSpeed, (|/ ((fuel)/3.14))*6 as fuel from " + TABLE + " where acceleration<>0 and avgAcceleration<>0 and km > 0 and vehicleid= "+ str(v[0]) + ")s where fuel > 0;").getresult()		
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
	res = con.query("select a.vehicleid, acc::float/c as a, steady::float/c as s, dec::float/c as d, stopped::float/c as st, idle::float/c as i, o::float/c as o from (select vehicleid, count(case when acceleration3<0 and cruise is false then 1 end) as dec, count(case when cruise is true then 1 end) as steady, count(case when acceleration3>0 and cruise is false then 1 end) as acc, count(case when stopped=1 and idle=0 then 1 end) as stopped, count(case when idle=1 then 1 end) as idle, count(case when acceleration3=0 and cruise is false and stopped =0 then 1 end) as o from g_gps_can_data where dirty is false group by vehicleid)a,(select vehicleid,count(*) as c from g_gps_can_data where dirty is false group by vehicleid)t where a.vehicleid=t.vehicleid;").getresult()
	
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

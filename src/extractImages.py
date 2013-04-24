import pg, sys, os, csv

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


#clusters = [4,7.7]

#Letter, color, pattern
patterns = {1: ['b', 'red', '1'], 2: ['c', 'blue', '2'], 3: ['a', 'green', '4'], 4: ['d', '#BB00FF', '5']}

print "set terminal png size 1000,500;"

if TYPE == 'km_pr_l':
	clusters = []
	clusters.append(con.query('select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+ TABLE + ';').getresult()[0][0])
	clusters.append(con.query('select avg(km_pr_l) from '+TABLE+' where km_pr_l > (select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+TABLE+')').getresult()[0][0])

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
	print "set ylabel 'km/l'"
	print "set xlabel 'Trips'"
	print "set yrange[0:12]"
	s = "plot "
	for v in vehicles:
		vid = str(v[0])
		s+= "'"+path + "data/" + vid + "_kmldata.csv' lc rgb '" + patterns[v[0]][1]+ "' title '" + vid + "', "

	print s + ""+str(clusters[0])+" lw 2 lc rgb \"black\" notitle, "+str(clusters[1])+" lw 2 lc rgb \"black\" notitle"
	
elif TYPE == 'TripsKmlCluster':


	res = con.query("select round(km_pr_l::decimal*4,0)/4 as round, count(*) from " + TABLE + " group by round order by round;").getresult()
	output = open(path +'data/TripsKmlCluster.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/TripsKmlCluster.png';"
	print "set ylabel 'Number of trips"
	print "set xlabel 'km/l '"
	print "set xtic 0.5"
	print "set arrow from 3.5,0 to 3.5,300 lw 2 nohead"
	print "set arrow from 8.125,0 to 8.125,300 lw 2 nohead"
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

elif TYPE == 'idle2':
	clusters = []
	clusters.append(con.query('select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+ TABLE + ';').getresult()[0][0])
	clusters.append(con.query('select avg(km_pr_l) from '+TABLE+' where km_pr_l > (select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+TABLE+')').getresult()[0][0])
	
	res = con.query("select round((idle_percentage*100)/5)*5 as round,count(case when km_pr_l <"+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l < "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " group by round order by round;").getresult()
	
	output = open(path + 'data/idle2.csv', 'w+')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/idle2.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'Percent of trip in idle (%)'"
	print "set xtics 10"
	print "set yrange[0:100]"
	#print "set xrange[0:40]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set logscale y2 10"
	print "set key opaque"
	print "plot '" + path + "data/idle2.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '" + path + "data/idle2.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '" + path + "data/idle2.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/idle2.csv' using 1:5 with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"
	
elif TYPE == 'idle3':
	clusters = []
	clusters.append(con.query('select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+ TABLE + ';').getresult()[0][0])
	clusters.append(con.query('select avg(km_pr_l) from '+TABLE+' where km_pr_l > (select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+TABLE+')').getresult()[0][0])
	
	res = con.query("select * from (select round(idle_time::numeric/50,0)*50 as idle, count(case when km_pr_l <"+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l < "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " group by idle order by idle)a where idle>=250;").getresult()
	
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
#	print "set logscale y2 10"
	print "set key opaque"
	print "set xtics 100"
	
	
	print "plot '" + path + "data/idle3.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/idle3.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/idle3.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/idle3.csv' using 1:5 with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"

elif TYPE == 'normalRoad':
	clusters = []
	clusters.append(con.query('select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+ TABLE + ';').getresult()[0][0])
	clusters.append(con.query('select avg(km_pr_l) from '+TABLE+' where km_pr_l > (select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+TABLE+')').getresult()[0][0])
	
	res = con.query("select round((PNormalRoad)::numeric,2),count(case when km_pr_l <"+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l < "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " where total_km >= 0.1 and PNormalRoad is not null  group by round order by round;").getresult()
	
	output = open(path + 'data/normalRoad.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/normalRoad.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'Normal Road P'"
	print "set yrange[0:100]"
	print "set xrange[0:]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set key opaque"
	print "plot '" + path + "data/normalRoad.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/normalRoad.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/normalRoad.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/normalRoad.csv' using 1:5 with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"

elif TYPE == 'smallRoad':
	clusters = []
	clusters.append(con.query('select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+ TABLE + ';').getresult()[0][0])
	clusters.append(con.query('select avg(km_pr_l) from '+TABLE+' where km_pr_l > (select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+TABLE+')').getresult()[0][0])
	
	res = con.query("select round((PSmallRoad)::numeric,2),count(case when km_pr_l <"+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l < "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " where total_km >= 0.1 and PSmallRoad is not null group by round order by round;").getresult()
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
	print "plot '" + path + "data/smallRoad.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/smallRoad.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/smallRoad.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/smallRoad.csv' using 1:5 with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"

elif TYPE == 'moterRoad':
	clusters = []
	clusters.append(con.query('select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+ TABLE + ';').getresult()[0][0])
	clusters.append(con.query('select avg(km_pr_l) from '+TABLE+' where km_pr_l > (select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+TABLE+')').getresult()[0][0])
	
	res = con.query("select round((pmoterroad)::numeric,2),count(case when km_pr_l <"+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l < "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " where total_km >= 0.1 and pmoterroad is not null group by round order by round;").getresult()
	output = open(path + 'data/moterRoad.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/moterRoad.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'Motor Road P'"
	print "set yrange[0:100]"
	print "set xrange[0:]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set key opaque"
	print "plot '" + path + "data/moterRoad.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/moterRoad.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/moterRoad.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/moterRoad.csv' using 1:5 with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"

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
	#print "set logscale y 10"
	print "plot '" + path + "data/cruiseCounter0.csv' using 1:($2/1000) with lines lw 3 title '+/- 0 km/h','" + path + "data/cruiseCounter1.csv' using 1:($2/1000) with lines lw 3 title '+/- 1 km/h','" + path + "data/cruiseCounter2.csv' using 1:($2/1000) with lines lw 3 title '+/- 2 km/h', '" + path + "data/cruiseCounter3.csv' using 1:($2/1000) with lines lw 3 title '+/- 3 km/h','" + path + "data/cruiseCounter4.csv' using 1:($2/1000) with lines lw 3 title '+/- 4 km/h'"

elif TYPE == 'cruisep':
	clusters = []
	clusters.append(con.query('select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+ TABLE + ';').getresult()[0][0])
	clusters.append(con.query('select avg(km_pr_l) from '+TABLE+' where km_pr_l > (select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+TABLE+')').getresult()[0][0])
	
	res = con.query("select * from (select round((cruise_percentage)::numeric,2)*100 as round,count(case when km_pr_l <"+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l < "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) as c from " + TABLE + " where total_km >= 0.1 group by round order by round)a where c > 10;").getresult()
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

	print "plot '" + path + "data/cruisep.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/cruisep.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/cruisep.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/cruisep.csv' using 1:5 with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"




elif TYPE == 'trafficlight':
	clusters = []
	clusters.append(con.query('select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+ TABLE + ';').getresult()[0][0])
	clusters.append(con.query('select avg(km_pr_l) from '+TABLE+' where km_pr_l > (select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+TABLE+')').getresult()[0][0])
	
	res = con.query("select round((tlcounter)::numeric,1),count(case when km_pr_l <"+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l < "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " where total_km >= 0.1 group by round order by round;").getresult()
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
	print "plot '" + path + "data/trafficlight.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/trafficlight.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/trafficlight.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/trafficlight.csv' using 1:5 with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"

elif TYPE == 'trafficlightgreen':
	clusters = []
	clusters.append(con.query('select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+ TABLE + ';').getresult()[0][0])
	clusters.append(con.query('select avg(km_pr_l) from '+TABLE+' where km_pr_l > (select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+TABLE+')').getresult()[0][0])
	
	res = con.query("select round((tlgreencounter)::numeric,1),count(case when km_pr_l <"+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l < "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " where total_km >= 0.1 group by round order by round;").getresult()
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
	
	print "plot '" + path + "data/trafficlightgreen.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/trafficlightgreen.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/trafficlightgreen.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/trafficlightgreen.csv' using 1:5 with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"

elif TYPE == 'trafficlightred':
	clusters = []
	clusters.append(con.query('select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+ TABLE + ';').getresult()[0][0])
	clusters.append(con.query('select avg(km_pr_l) from '+TABLE+' where km_pr_l > (select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+TABLE+')').getresult()[0][0])
	
	res = con.query("select round((tlredcounter)::numeric,1),count(case when km_pr_l <"+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l < "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " where total_km >= 0.1 group by round order by round;").getresult()
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
	print "plot '" + path + "data/trafficlightred.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/trafficlightred.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/trafficlightred.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/trafficlightred.csv' using 1:5 with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"

elif TYPE == 'trafficlightratio':
	clusters = []
	clusters.append(con.query('select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+ TABLE + ';').getresult()[0][0])
	clusters.append(con.query('select avg(km_pr_l) from '+TABLE+' where km_pr_l > (select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+TABLE+')').getresult()[0][0])
	
	res = con.query("select round((tlredcounter/tlcounter)::numeric,1),count(case when km_pr_l <"+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l < "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " where total_km >= 0.1 and tlcounter > 0 group by round order by round;").getresult()
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
	print "plot '" + path + "data/trafficlightratio.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/trafficlightratio.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/trafficlightratio.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/trafficlightratio.csv' using 1:5 with lines lw 3 lc rgb \"#ffff00\" title 'Number of trips' axes x1y2"


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
	print "set ylabel 'Number of idle records"
	print "set xlabel 'Radius from Traficlight (m)'"
	#print "set logscale y 10"
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
	
elif TYPE == 'idleRange2':
	vehicles = con.query("select distinct vehicleid from " + TABLE + ";").getresult()
	for v in vehicles:
		res = con.query("select * from (select (case when round(stopped/100)*100=0 then 1 else round(stopped/100)*100 end)::integer as idle, count(*) from "+ TABLE + " where vehicleid =" + str(v[0]) + " group by idle order by idle)a where count > 1;").getresult()
	
		output = open(path + 'data/'+str(v[0])+'idleRange2.csv', 'w+')
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for r in res:
			writer.writerow(r)

	boxwidth= 100.0/(len(vehicles)+1)
	print "set output '" + path + "images/idleRange2.png';"
	print "set ylabel 'Number of records';"
	print "set xlabel 'Idle range (s)'"
	print "set style fill solid border -1"
	print "set boxwidth " + str(boxwidth)
	print "set xtic rotate by -45 scale 0"
	print "set logscale y 10"
	print "set xr [-10:]"
	print "set xtics 100"
	
	offset = 0
	s = "plot "
	for v in vehicles:
		s += "'" + path + "data/"+str(v[0]) + "idleRange2.csv' using ($1+"+ str(offset) + "):2 with boxes lc rgb '" + patterns[v[0]][1]+ "' fs pattern " + patterns[v[0]][2] + " title '" + str(v[0]) + "' ,"
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
	

elif TYPE == 'accelerationRanges':
	vehicles = con.query("select vehicleid, count(*) from " + TABLE + " where dirty = false group by vehicleid order by vehicleid;").getresult()
	
	granularity = 0.25
	for v in vehicles:
		res = con.query("select * from (select round(acceleration2::decimal*4, 0)/4 as acc, count(*)::float as c from "+ TABLE + " where vehicleid =" + str(v[0]) + " and cruise = false and dirty = false group by acc order by acc)a where (acc > 0.1 or acc < -0.1)  and c > 800;").getresult()
		output = open(path + 'data/'+str(v[0])+'accelerationRanges.csv', 'w+')
		for r in res:
			print >> output, str(r[0]) + " " + str(float(r[1])/float(v[1]))
	boxwidth= (float(granularity))/(len(vehicles)+1)
	print "set output '" + path + "images/accelerationRanges.png';"
	print "set ylabel 'Number of records'"
	print "set xlabel 'Acceleration (m/s^2)'"
	print "set style fill solid border -1"
	print "set boxwidth " + str(boxwidth)
	print "set xtic rotate by -45 scale 0"
	print "set xtics " + str(float(granularity))
	print "set xrange[:]"
	
	offset = 0
	s = "plot "
	for v in vehicles: #fs pattern " + patterns[v[0]][2] + " 
		s += "'" + path + "data/"+str(v[0]) + "accelerationRanges.csv' using ($1+"+ str(offset) + "):2 with boxes lc rgb '" + patterns[v[0]][1]+ "'  title '" + str(v[0]) + "',"
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

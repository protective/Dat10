import pg, sys, os, csv

USER = 'd103'
DB = 'gps_can'
TABLE = 'trip_data'
TYPE = sys.argv[1]
if len(sys.argv) > 2:
	TABLE = sys.argv[2]
path = ''
clusters = [6,8]


if (False):
	USER = 'sabrine'
	path = ''

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

print "set terminal png size 1000,500;"

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
	print "set ylabel 'km/l';"
	print "set xlabel 'Trips';"

	s = "plot "
	for v in vehicles:
		vid = str(v[0])
		s+= "'"+path + "data/" + vid + "_kmldata.csv' title '" + vid + "', "

	print s + ""+str(clusters[0])+" lw 2 notitle, "+str(clusters[1])+" lw 2 notitle"
	
elif TYPE == 'TimeTrips':
	print "set output '" + path + "images/TimeTrips.png';"
	print "set ylabel 'Number of trips"
	print "set xlabel 'Timeframe (s)'"
	print "set yrange[0:]"

	print "plot '" + path + "data/trajectoryTime.csv' using 1:3 with lines lw 3 notitle"

elif TYPE == 'LengthTrips': 
	print "set output '" + path + "images/TripsLength.png';"
	print "set ylabel 'Number of trips"
	print "set xlabel 'Minimum number of data records'"
	print "set yrange[0:]"

	print "plot '" + path + "data/trajectoryLength.csv' using 2:3 with lines lw 3 notitle"
	
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
	res = con.query("select round((idle_percentage*100)::numeric,0),count(case when km_pr_l <="+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l <= "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " group by round order by round;").getresult()
	
	output = open(path + 'data/idle2.csv', 'w+')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/idle2.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'Percent of trip in idle (%)'"
	print "set yrange[0:100]"
	print "set xrange[0:40]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set key outside"
	print "plot '" + path + "data/idle2.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '" + path + "data/idle2.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '" + path + "data/idle2.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/idle2.csv' using 1:5 with lines lw 3 title 'Number of trips' axes x1y2"
	
elif TYPE == 'idle3':
	res = con.query("select round(idle_time::numeric/100,0)*100 as idle, count(case when km_pr_l <="+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l <= "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " group by idle order by idle;").getresult()
	
	output = open(path + 'data/idle3.csv', 'w+')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "images/idle3.png';"
	print "set ylabel 'Class distribution (%)'"
	print "set xlabel 'Idle time (s)'"
	print "set yrange[0:100]"
	print "set xrange[0:1500]"
	print "set y2tics"
	print "set y2label 'Number of trips'"
	print "set key outside"
	print "plot '" + path + "data/idle3.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/idle3.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/idle3.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/idle3.csv' using 1:5 with lines lw 3 title 'Number of trips' axes x1y2"

elif TYPE == 'normalRoad':
	res = con.query("select round((PNormalRoad*10)::numeric,0),count(case when km_pr_l <="+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l <= "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " group by round order by round;").getresult()
	
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
	print "set key outside"
	print "plot '" + path + "data/normalRoad.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/normalRoad.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/normalRoad.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/normalRoad.csv' using 1:5 with lines lw 3 title 'Data points' axes x1y2"

elif TYPE == 'smallRoad':
	res = con.query("select round((PSmallRoad*10)::numeric,0),count(case when km_pr_l <="+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l <= "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " group by round order by round;").getresult()
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
	print "set key outside"
	print "plot '" + path + "data/smallRoad.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/smallRoad.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/smallRoad.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/smallRoad.csv' using 1:5 with lines lw 3 title 'Data points' axes x1y2"

elif TYPE == 'moterRoad':
	res = con.query("select round((pmoterroad*10)::numeric,0),count(case when km_pr_l <="+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l <= "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " group by round order by round;").getresult()
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
	print "set key outside"
	print "plot '" + path + "data/moterRoad.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/moterRoad.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/moterRoad.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/moterRoad.csv' using 1:5 with lines lw 3 title 'Data points' axes x1y2"


elif TYPE == 'trafficlight':
	
	res = con.query("select round((tlcounter)::numeric,1),count(case when km_pr_l <="+str(clusters[0])+" then 1 end)::float/count(*)*100 as low,count(case when km_pr_l <= "+str(clusters[1])+" then 1 end)::float/count(*)*100 as medium,100 as high ,count(*) from " + TABLE + " group by round order by round;").getresult()
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
	print "set key outside"
	print "plot '" + path + "data/trafficlight.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, '"+path+"data/trafficlight.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, '"+path+"data/trafficlight.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/trafficlight.csv' using 1:5 with lines lw 3 title 'Data points' axes x1y2"




elif TYPE == 'idleDuration':
	print "set output '" + path + "images/idleDuration.png';"
	print "set ylabel 'Number of idle records"
	print "set xlabel 'Minimum duration'"
	print "plot '" + path + "data/idleDuration.csv' with lines lw 3 notitle"

elif TYPE == 'idleTime':
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
	
elif TYPE == 'idleRange':
	res = con.query("select idle, count(*) from (select round(count(case when idleRange=1 then 1 end)/10)*10 as idle from " + TABLE + " group by tid)a group by idle order by idle;").getresult()
	
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
		res = con.query("select (case when round(idleRange/100)*100=0 then 1 else round(idleRange/100)*100 end) as idle, count(*) from "+ TABLE + " where vehicleid =" + str(v[0]) + " group by idle order by idle;").getresult()
	
		output = open(path + 'data/'+str(v[0])+'idleRange2.csv', 'w+')
		writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for r in res:
			writer.writerow(r)

	print "set output '" + path + "images/idleRange2.png';"
	print "set ylabel 'Number of records';"
	print "set xlabel 'Idle range (s)'"
	print "set style data histogram"
	print "set style histogram cluster gap 1"
	print "set style fill solid border -1"
	print "set boxwidth 0.9"
	print "set xtic rotate by -45 scale 0"
	print "set logscale y 2"
	
	s = "plot "
	for v in vehicles:
		s += "'" + path + "data/"+str(v[0]) + "idleRange2.csv' using 2:xtic(1) title '" + str(v[0]) + "',"
	print s[:-1]

elif TYPE == 'idleRange3':
	res = con.query("select idleRange, fuel, vehicleid from "+TABLE+" where idleRange>=100;").getresult()
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
	print "set xrange[100:]"
	
	s = "plot "
	for v in vehicles:
		s += "'" + path + "data/"+str(v) + "idleRange3.csv' using 1:2 title '" + str(v) + "',"
	print s[:-1]

elif TYPE == 'idlePercent':
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
	print "set yrange[:30]"

	s = "plot "
	s+= "'" + path + "images/" + TYPE + "_high_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"green\" title 'High' , "
	s+= "'" + path + "images/" + TYPE + "_medium_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"blue\" title 'Medium', "
	s+= "'" + path + "images/" + TYPE + "_low_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"red\" title 'Low'"
	print s

else:
	val = TYPE + '*100, km_pr_l as val, |/ (total_fuel/3.14)'
	where= ''
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

	print "set output '" + path + "images/" + TYPE + "Trips.png';"
	print "set ylabel 'km/l';"
	print "set xlabel '"+ TYPE + "';"

	s = "plot "
	s+= "'" + path + "images/" + TYPE + "_high_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"green\" title 'High' , "
	s+= "'" + path + "images/" + TYPE + "_medium_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"blue\" title 'Medium', "
	s+= "'" + path + "images/" + TYPE + "_low_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"red\" title 'Low'"
	print s

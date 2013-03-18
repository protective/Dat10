import pg, sys, os, csv

USER = 'd103'
DB = 'gps_can'
TABLE = 'trip_data'
TYPE = sys.argv[1]
path = 'Dat10/src/'

if (False):
	USER = 'sabrine'
	path = ''

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

print "set terminal png size 1000,500;"

if TYPE == 'km_pr_l':
	vehicles = con.query("select distinct vehicleid from " + TABLE + ";").getresult()

	for v in vehicles:
		vid = str(v[0])
		res = con.query("select " + TYPE + " from " + TABLE + " where vehicleid=" + vid + " order by tid;").getresult()
		output = open(path + 'images/' + vid + '_' + TYPE + '_data.csv', 'wb')
		for r in res:
			print>> output, r[0]
 
	print "set output '" + path + "images/" + TYPE + "Trips.png';"
	print "set ylabel 'km/l';"
	print "set xlabel 'Trips';"

	s = "plot "
	for v in vehicles:
		vid = str(v[0])
		s+= path + "'images/" + vid + '_' + TYPE + "_data.csv' title '" + vid + "', "

	print s + "4 lw 2 notitle, 8 lw 2 notitle"

elif TYPE == 'TimeTrips':
	print "set output '" + path + "images/" + TYPE + ".png';"
	print "set ylabel 'Number of trips"
	print "set xlabel 'Time??'"

	print "plot '" + path + "data/noTrajectories.csv' with lines lw 3 notitle"

elif TYPE == 'LengthTrips': 
	print "set output '" + path + "images/" + TYPE + ".png';"
	print "set ylabel 'Number of trips"
	print "set xlabel 'Minimum number of data records'"

	print "plot '" + path + "data/noTripsLength.csv' with lines lw 3 notitle"
	
elif TYPE == 'minFuel':
	print "set output '" + path + "images/minFuel.png';"
	print "set ylabel 'Number of trips"
	print "set xlabel 'Minimum fuel consumption'"
	output = open(path +'data/minFuel.csv', 'wb')
	for i in range(0,20, 1):
		step = float(i)/10
		res = con.query("select count(*)-count(case when total_fuel < " + str(step) + " then 1 end) from trip_data;").getresult()
		print >>output, str(step) + " " + str(res[0][0])

	print "plot '" + path + "data/minFuel.csv' with lines lw 3 notitle"

elif TYPE == 'TripLengthKml':
	res = con.query("select total_km, km_pr_l from trip_data;").getresult()
	#res = con.query("select EXTRACT(EPOCH FROM t), km_pr_l from trip_data, (select tid, (max(timestamp)-min(timestamp))t from a_gps_can_data group by tid)a where trip_data.tid=a.tid;").getresult()
	output = open(path +'data/tripLengthKml.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for r in res:
		writer.writerow(r)

	
	print "set output '" + path + "images/TripLengthKml.png';"
	print "set ylabel 'km/l"
	print "set xlabel 'km'"

	print "plot '" + path + "data/tripLengthKml.csv' notitle"

elif TYPE == 'idle2':
	res = con.query("""
	select round(idle_percentage*100), 
		count(case when km_pr_l <=4 then 1 end)::float/count(*)*100 as low,
		count(case when km_pr_l < 8 then 1 end)::float/count(*)*100 as medium,
		100 as high ,
		count(*) 
	from trip_data where round <=60 group by round order by round;
	""").getresult()
	
	output = open(path + 'data/idle2.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)

	print "set output '" + path + "/images/idle2.png';"
	print "set ylabel 'Percent'"
	print "set xlabel 'Percent idle'"
	print "set yrange[0:100]"
	print "set xrange[0:100]"
	print "set y2tics"
	print "set y2label 'Number of datapoints'"
	print "set key outside"
	print "plot '" + path + "data/idle2.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 2, 'data/idle2.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, 'data/idle2.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 1, '" + path + "data/idle2.csv' using 1:5 with lines lw 3 title 'Data points' axes x1y2"

else:
	val = TYPE + ', km_pr_l as val, |/ (total_fuel/3.14)'
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
	if (TYPE == 'stopngo'):
		print "set xrange[-3:]"
	elif (TYPE == 'acckm'):
		print "set xrange[-50:]"

	else:
		print "set xrange[-0.1:]"

	s = "plot "
	s+= "'" + path + "images/" + TYPE + "_high_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"green\" title 'High' , "
	s+= "'" + path + "images/" + TYPE + "_medium_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"blue\" title 'Medium', "
	s+= "'" + path + "images/" + TYPE + "_low_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"red\" title 'Low'"
	print s

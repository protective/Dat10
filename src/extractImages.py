import pg, sys, os, csv

USER = 'd103'
DB = 'gps_can'
TABLE = 'trip_data'
TYPE = sys.argv[1]

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

print "set terminal png size 1000,500;"

if TYPE == 'km_pr_l':
	vehicles = con.query("select distinct vehicleid from " + TABLE + ";").getresult()

	for v in vehicles:
		vid = str(v[0])
		res = con.query("select " + TYPE + " from " + TABLE + " where vehicleid=" + vid + " order by tid;").getresult()
		output = open('images/' + vid + '_' + TYPE + '_data.csv', 'wb')
		for r in res:
			print>> output, r[0]
 
	print "set output 'images/" + TYPE + "Trips.png';"
	print "set ylabel 'km/l';"
	print "set xlabel 'Trips';"

	s = "plot "
	for v in vehicles:
		vid = str(v[0])
		s+= "'images/" + vid + '_' + TYPE + "_data.csv' title '" + vid + "', "

	print s + "4 lw 2 notitle, 8 lw 2 notitle"

elif TYPE == 'TimeTrips':
	print "set output 'images/" + TYPE + ".png';"
	print "set ylabel 'Number of trips"
	print "set xlabel 'Time??'"

	print "plot 'data/noTrajectories.csv' with lines lw 3 notitle"

elif TYPE == 'LengthTrips': 
	print "set output 'images/" + TYPE + ".png';"
	print "set ylabel 'Number of trips"
	print "set xlabel 'Minimum number of seqments'"

	print "plot 'data/noTripsLength.csv' with lines lw 3 notitle"

elif TYPE == 'TripLengthKml':
	res = con.query("select total_km, km_pr_l from trip_data;").getresult()
	#res = con.query("select EXTRACT(EPOCH FROM t), km_pr_l from trip_data, (select tid, (max(timestamp)-min(timestamp))t from a_gps_can_data group by tid)a where trip_data.tid=a.tid;").getresult()
	output = open('data/tripLengthKml.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for r in res:
		writer.writerow(r)

	
	print "set output 'images/TripLengthKml.png';"
	print "set ylabel 'km/l"
	print "set xlabel 'km'"

	print "plot 'data/tripLengthKml.csv' notitle"

elif TYPE == 'test':
	print 'plot 2'

elif TYPE == 'idle2':
	res = con.query("""
	select round(idle_percentage*100), 
		count(case when km_pr_l <=4 then 1 end)::float/count(*)*100 as low,
		count(case when km_pr_l < 8 then 1 end)::float/count(*)*100 as medium,
		100 as high  
	from trip_data group by round order by round;
	""").getresult()
		
	output = open('data/idle2.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for r in res:
		writer.writerow(r)
	
	print "set output 'images/idle2.png';"
	print "set yrange[0:100]"
	print "set key outside"
	print """plot 'data/idle2.csv' using 1:4 t \"High\" w filledcurves x1 linestyle 4, 'data/idle2.csv' using 1:3 t \"Medium\" w filledcurves x1 linestyle 3, 'data/idle2.csv' using 1:2 t \"Low\" w filledcurves x1 linestyle 2"""
	

else:
	val = TYPE + ', km_pr_l as val, total_fuel'
	where= ''
	res = con.query("select " + val + " from " + TABLE + " where km_pr_l < 4  order by val;").getresult()
	output = open('images/' + TYPE + '_low_data.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for r in res:
		writer.writerow(r)

	res = con.query("select " + val + " from " + TABLE + " where km_pr_l >= 4 and km_pr_l < 8 order by val;").getresult()
	output = open('images/' + TYPE + '_medium_data.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for r in res:
		writer.writerow(r)

	res = con.query("select " + val + " from " + TABLE + " where km_pr_l > 8 order by val;").getresult()
	output = open('images/' + TYPE + '_high_data.csv', 'wb')
	writer = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for r in res:
		writer.writerow(r)

	print "set output 'images/" + TYPE + "Trips.png';"
	print "set ylabel 'km/l';"
	print "set xlabel '"+ TYPE + "';"
	if (TYPE == 'stopngo'):
		print "set xrange[-3:]"
	elif (TYPE == 'acckm'):
		print "set xrange[-50:]"

	else:
		print "set xrange[-0.1:]"

	s = "plot "
	s+= "'images/" + TYPE + "_high_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"green\" title 'High' , "
	s+= "'images/" + TYPE + "_medium_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"blue\" title 'Medium', "
	s+= "'images/" + TYPE + "_low_data.csv' using 1:2:3 with points lt 1 pt 6 ps variable linecolor rgb \"red\" title 'Low'"
	print s

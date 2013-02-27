import pg, sys, os, csv

USER = os.getlogin()
DB = 'gps_can'
TABLE = 'trip_data'
TYPE = sys.argv[1]

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

if TYPE == 'km_pr_l':
	vehicles = con.query("select distinct vehicleid from " + TABLE + ";").getresult()

	for v in vehicles:
		vid = str(v[0])
		res = con.query("select " + TYPE + " from " + TABLE + " where vehicleid=" + vid + " order by tid;").getresult()
		output = open('images/' + vid + '_' + TYPE + '_data.csv', 'wb')
		for r in res:
			print>> output, r[0]

	print "set terminal png size 1000,500;set y2tics;" 
	print "set output 'images/" + TYPE + "Trips.png';"

	s = "plot "
	for v in vehicles:
		vid = str(v[0])
		s+= "'images/" + vid + '_' + TYPE + "_data.csv' title '" + vid + "', "

	print s + "4 lw 2 notitle, 8 lw 2 notitle"

else:
	if TYPE == 'acckm':
		val = 'round(cast(' + TYPE + ' as numeric)/10)*10'
	elif TYPE == 'stopngo':
		val = 'round(cast(' + TYPE + ' as numeric))'
	else:
		val = 'round(cast(' + TYPE + ' as numeric), 2)'

	res = con.query("select " + val + "idle, count(*) from " + TABLE + " where km_pr_l < 4 group by idle order by idle;").getresult()
	output = open('images/' + TYPE + '_low_data.csv', 'wb')
	spamwriter = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for r in res:
		spamwriter.writerow(r)
	
	res = con.query("select " + val + "idle, count(*) from " + TABLE + " where km_pr_l >= 4 and km_pr_l < 8 group by idle order by idle;").getresult()
	output = open('images/' + TYPE + '_medium_data.csv', 'wb')
	spamwriter = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for r in res:
		spamwriter.writerow(r)
	
	res = con.query("select " + val + "idle, count(*) from " + TABLE + " where km_pr_l > 8 group by idle order by idle;").getresult()
	output = open('images/' + TYPE + '_high_data.csv', 'wb')
	spamwriter = csv.writer(output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for r in res:
		spamwriter.writerow(r)

	print "set terminal png size 1000,500;set y2tics;" 
	print "set output 'images/" + TYPE + "Trips.png';"

	s = "plot "
	s+= "'images/" + TYPE + "_high_data.csv' title 'High', "
	s+= "'images/" + TYPE + "_medium_data.csv' title 'Medium', "
	s+= "'images/" + TYPE + "_low_data.csv' title 'Low'"
	print s


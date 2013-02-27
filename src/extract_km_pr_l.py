import pg, sys, os, csv

USER = os.getlogin()
DB = 'gps_can'
TABLE = 'trip_data'
TYPE = 'km_pr_l'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

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

print s + ", 4 lw 2 notitle, 8 lw 2 notitle"


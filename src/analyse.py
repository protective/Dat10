import pg, sys, os, csv

TID = sys.argv[1]

USER = os.getlogin()
DB = 'gps_can'
TABLE = 'a_gps_can_data'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

res = con.query("select extract('epoch' from age(timestamp, (select min	(timestamp) from " + TABLE + " where tid=" + TID + "))), totalconsumed-(select min(totalconsumed) from " + TABLE + " where tid=" + TID + 	"), speed, rpm, acceleration from " + TABLE + " where tid=" + TID + " order by timestamp;").getresult()

output = open('images/' + TID + '_data.csv', 'wb')

s = ""
for r in res:
	for i in r:
		s += str(i) + " "
	s+='\n'
print >> output, s

print "set terminal png size 1000,500;set y2tics;" 
print "set output 'images/" + TID + "_FuelSpeed.png';"
print "plot 'images/" + TID + "_data.csv' using 1:2 with lines title 'Fuel', 'images/" + TID + "_data.csv' using 1:3 with lines axes x1y2 title 'Speed'"

print "set output 'images/" + TID + "_FuelRPM.png';"
print "plot 'images/" + TID + "_data.csv' using 1:2 with lines title 'Fuel', 'images/" + TID + "_data.csv' using 1:4 with lines axes x1y2 title 'RPM'"

print "set output 'images/" + TID + "_FuelAcc.png';"
print "plot 'images/" + TID + "_data.csv' using 1:2 with lines title 'Fuel', 'images/" + TID + "_data.csv' using 1:5 with lines axes x1y2 title 'Acceleration'"

print "set output 'images/" + TID + "_SpeedAcc.png';"
print "plot 'images/" + TID + "_data.csv' using 1:3 with lines title 'Speed' lc rgb \"blue\", 'images/" + TID + "_data.csv' using 1:5 with lines axes x1y2 title 'Acceleration' lc rgb \"red\""





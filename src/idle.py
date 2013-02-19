import pg , math, sys
#1 = idle
#2 = stop
#3 = run
con = pg.connect(dbname='gps_can', host='localhost', user='karsten',passwd='F1ff')

try:
	con.query('alter table a_gps_can_data add column idle int;')
finally:

	con.query("update a_gps_can_data set idle = 1 where speed < 10 and rpm <= 900;")
	con.query("update a_gps_can_data set idle = 2 where rpm = 0;")
	print "holy"
	con.query("update a_gps_can_data set idle = 3 where idle != 1 and idle !=2;")
	

#
#








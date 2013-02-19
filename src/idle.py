import pg , math, sys

con = pg.connect(dbname='gps_can', host='localhost', user='karsten',passwd='F1ff')

try:
	con.query('alter table a_gps_can_data add column idle varchar;')
finally:

	#con.query("update a_gps_can_data set idle = 'Idle' where speed < 10 and rpm <= 900;")
	con.query("update a_gps_can_data set idle = 'Stop' where rpm = 0;")
	print "holy"
	con.query("update a_gps_can_data set idle = 'Run' where idle != 'Stop' and idle !='Idle';")
	

#
#








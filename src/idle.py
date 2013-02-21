import os, pg , math, sys
#1 = idle
#2 = stop
#3 = run
con = pg.connect(dbname='gps_can', host='localhost', user=os.getlogin(),passwd='F1ff')

try:
	con.query('alter table a_gps_can_data drop idle;')
finally:
	con.query('alter table a_gps_can_data add column idle int not null default 0;')

print 'Setting idle state'
con.query("update a_gps_can_data set idle = 1 where speed < 10 and rpm <= 900;")
print 'Setting stopped state'
con.query("update a_gps_can_data set idle = 2 where rpm = 0;")
print "Setting running state"
con.query("update a_gps_can_data set idle = 3 where idle != 1 and idle !=2;")
	
print "Creating index"
con.query("Create index idle_a_gps_can_data_idx on a_gps_can_data (idle);")


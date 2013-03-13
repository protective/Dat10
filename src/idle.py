import os, pg , math, sys
#1 = idle
#0 = run
con = pg.connect(dbname='gps_can', host='localhost', user='d103',passwd='F1ff')

con.query('alter table a_gps_can_data drop IF EXISTS idle;')
con.query('alter table a_gps_can_data add column idle int not null default 0;')

print 'Setting idle state'
con.query("update a_gps_can_data set idle = 1 where speed = 0 and rpm > 0;")
#print "Setting running state"
#con.query("update a_gps_can_data set idle = 3 where idle != 1 and idle !=2;")
	
print "Creating index"
con.query("Create index idle_a_gps_can_data_idx on a_gps_can_data (idle);")


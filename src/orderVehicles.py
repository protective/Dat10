import pg, sys,os

USER = os.getlogin()
DB = 'gps_can'
OLD_TABLE = 'a_gps_can_data'
TABLE = 'trip_data'

print "Connecting to " + DB
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

res = con.query('select vehicleid, avg(km_pr_l), sum(total_km) as km from trip_data where km_pr_l is not null group by vehicleid order by avg desc;').getresult()

print res

import pg, sys,os

USER = os.getlogin()
DB = 'gps_can'
OLD_TABLE = 'a_gps_can_data'
TABLE = 'trip_data'

print "Connecting to " + DB
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

if (False):
	print 'Setting up ' + TABLE
	con.query('drop table ' + TABLE + ';')
	con.query('create table ' + TABLE + '(vehicleid bigint, tid int);')
	con.query('insert into ' + TABLE + '(select distinct vehicleid, tid from ' + OLD_TABLE + ' where dirty is null and totalconsumed is not null and kmcounter is not null);')

if (False):
	print 'km pr liter'
	try:
		con.query('alter table ' + TABLE + ' drop km_pr_l;')
	finally:
		con.query('alter table ' + TABLE + ' add km_pr_l float;')
		con.query('update ' + TABLE + ' set km_pr_l = kml from (select tid, ((max(kmcounter)-min(kmcounter))/(case when (max(totalconsumed)-min(totalconsumed)) =0 then 1 else (max(totalconsumed)-min(totalconsumed)) end))kml from a_gps_can_data where totalconsumed is not null and kmcounter is not null and totalconsumed < 4000000 group by tid)s where ' + TABLE + '.tid=s.tid;')

print 'Percentage in idle'
try:
	con.query('alter table ' + TABLE + ' drop idle_percentage;')
finally:
	con.query('alter table ' + TABLE + ' add idle_percentage float;')
	con.query('update ' + TABLE + ' set idle_percentage = p from (select tid, (count(*)-count(case when idle!=1 then 1 end))::float/count(*) as p from ' + OLD_TABLE + ' where dirty is null group by tid)f where ' + TABLE + '.tid=f.tid;')


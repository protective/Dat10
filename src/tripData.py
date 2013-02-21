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
	
print 'Total km driven'
con.query('alter table ' + TABLE + ' drop total_km;')
con.query('alter table ' + TABLE + ' add total_km int;')
con.query('update ' + TABLE + ' set total_km = km from (select tid, (max(kmcounter)-min(kmcounter))km from ' + OLD_TABLE + ' where kmcounter is not null group by tid)s where ' + TABLE + '.tid=s.tid;')

print 'Total fuel consumed'
con.query('alter table ' + TABLE + ' drop total_fuel;')
con.query('alter table ' + TABLE + ' add total_fuel float;')
con.query('update ' + TABLE + ' set total_fuel = fuel from (select tid, (max(totalconsumed)-min(totalconsumed))fuel from ' + OLD_TABLE + ' where totalconsumed < 100000 and totalconsumed is not null group by tid)s where ' + TABLE + '.tid=s.tid;')
	
print 'km pr liter'
con.query('alter table ' + TABLE + ' drop km_pr_l;')
con.query('alter table ' + TABLE + ' add km_pr_l float;')
con.query('update ' + TABLE + ' set km_pr_l = total_km/total_fuel where total_fuel!=0;')
con.query('update ' + TABLE + ' set km_pr_l = null where total_fuel=0;')

print 'Percentage in idle'
con.query('alter table ' + TABLE + ' drop idle_percentage;')
con.query('alter table ' + TABLE + ' add idle_percentage float;')
con.query('update ' + TABLE + ' set idle_percentage = p from (select tid, (count(*)-count(case when idle!=1 then 1 end))::float/count(*) as p from ' + OLD_TABLE + ' where dirty is null group by tid)f where ' + TABLE + '.tid=f.tid;')


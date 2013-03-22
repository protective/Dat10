import pg, sys,os, time

USER = 'd103'
DB = 'gps_can'
OLD_TABLE = 'a_gps_can_data'
PREFIX = 'a'
if len(sys.argv) > 1:
	PREFIX = sys.argv[1]
OLD_TABLE = ""+PREFIX+"_gps_can_data"
TABLE = ""+PREFIX+"_trip_data"




print "Connecting to " + DB
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

print 'Setting up ' + TABLE
con.query('drop table if exists ' + TABLE + ';')
con.query('create table ' + TABLE + ' (vehicleid bigint, tid int);')
con.query('insert into ' + TABLE + ' (select distinct vehicleid, tid from ' + OLD_TABLE + ' where dirty is false and totalconsumed is not null and kmcounter is not null);')

print 'km pr liter'
con.query('alter table ' + TABLE + ' drop if exists km_pr_l;')
con.query('alter table ' + TABLE + ' add km_pr_l float;')
con.query('update ' + TABLE + ' set km_pr_l = kml from (select tid, ((max(kmcounter)-min(kmcounter))/(case when (max(totalconsumed)-min(totalconsumed)) =0 then 1 else (max(totalconsumed)-min(totalconsumed)) end))kml from ' + OLD_TABLE + ' where totalconsumed is not null and kmcounter is not null and totalconsumed < 4000000 and dirty is false group by tid)s where ' + TABLE + '.tid=s.tid;')
	
print 'Total km'
con.query('alter table ' + TABLE + ' drop if exists total_km')
con.query('alter table ' + TABLE + ' add total_km float;')
con.query('update ' + TABLE + ' set total_km = km from (select tid, (max(kmcounter)-min(kmcounter))km from ' + OLD_TABLE + ' where kmcounter is not null and dirty is false group by tid)s where ' + TABLE + '.tid=s.tid;')

print 'Total fuel'
con.query('alter table ' + TABLE + ' drop if exists total_fuel')
con.query('alter table ' + TABLE + ' add total_fuel float;')
con.query('update ' + TABLE + ' set total_fuel = fuel from (select tid, (max(totalconsumed)-min(totalconsumed))fuel from ' + OLD_TABLE + ' where totalconsumed is not null and totalconsumed < 4000000 and dirty is false group by tid)s where ' + TABLE + '.tid=s.tid;')

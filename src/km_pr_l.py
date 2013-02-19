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
	con.query('create table ' + TABLE + '(vehicleid bigint, tid int, km_pr_l float, total_km integer, total_fuel float);')
	con.query('insert into ' + TABLE + '(select distinct vehicleid, tid from ' + OLD_TABLE + ' where dirty is null and totalconsumed is not null and kmcounter is not null);')
	
print 'Updating km'
con.query('update ' + TABLE + ' set total_km = km from (select tid, (max(kmcounter)-min(kmcounter))km from ' + OLD_TABLE + ' where kmcounter is not null group by tid)s where ' + TABLE + '.tid=s.tid;')

print 'Updating fuel'
con.query('update ' + TABLE + ' set total_fuel = fuel from (select tid, (max(totalconsumed)-min(totalconsumed))fuel from ' + OLD_TABLE + ' where totalconsumed < 100000 and totalconsumed is not null group by tid)s where ' + TABLE + '.tid=s.tid;')
	
print 'Updating km pr liter'
con.query('update ' + TABLE + ' set km_pr_l = total_km/total_fuel where total_fuel!=0;')
con.query('update ' + TABLE + ' set km_pr_l = null where total_fuel=0;')


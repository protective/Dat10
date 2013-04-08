import pg , math, sys, os ,time

USER = 'd103'
DB = "gps_can"


PREFIX = 'a'
if len(sys.argv) > 1:
	PREFIX = sys.argv[1]
QUERY_TABLE = ""+PREFIX+"_gps_can_data"
TABLE = ""+PREFIX+"_trip_data"

MAP_TABLE = "osm_dk_20130214"




con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

con.query("alter table " + QUERY_TABLE + " drop IF EXISTS roadCategory;")
con.query('alter table ' + QUERY_TABLE + ' add roadCategory int;')

con.query('update '+PREFIX+'_gps_can_data as '+PREFIX+'  set roadcategory = (case when category in ( \'11\',\'12\')  then 1 when category in( \'13\',\'14\',\'15\',\'21\',\'31\') then 2 when category in (\'32\',\'33\',\'41\',\'42\',\'51\',\'63\') then 3 end) from gps_can_data as aa inner join ' + MAP_TABLE + ' on '+MAP_TABLE+'.segmentkey= aa.segmentkey where '+PREFIX+'.vehicleid= aa.vehicleid and '+PREFIX+'.timestamp=aa.timestamp;')

#con.query("create index "+MAP_TABLE+"_category_idx on "+MAP_TABLE+" (category);")


#s = 'update ' + QUERY_TABLE + ' set roadCategory = (case when category in ( \'11\',\'12\')  then 1 when category in( \'13\',\'14\',\'15\',\'21\',\'31\') then 2 when category in (\'41\',\'42\',\'51\',\'63\') then 3 end) from ' + MAP_TABLE + ' where ' + MAP_TABLE + '.segmentkey=' + QUERY_TABLE + '.segmentkey;'
#print s
#con.query(s)


con.query("alter table " + TABLE + " drop IF EXISTS PMoterRoad;")
con.query('alter table ' + TABLE + ' add PMoterRoad float;')
con.query("alter table " + TABLE + " drop IF EXISTS PNormalRoad;")
con.query('alter table ' + TABLE + ' add PNormalRoad float;')
con.query("alter table " + TABLE + " drop IF EXISTS PSmallRoad;")
con.query('alter table ' + TABLE + ' add PSmallRoad float;')


s = 'update ' + TABLE + '  set PMoterRoad = p from (select tid, count(case when roadCategory=1 then 1 end)::float/count(*) as p from ' + QUERY_TABLE + ' where dirty is false and stopped = 0 and roadCategory is not null group by tid)f where ' + TABLE + '.tid=f.tid;'
#print s
con.query(s)

s = 'update ' + TABLE + '  set PNormalRoad = p from (select tid, count(case when roadCategory=2 then 1 end)::float/count(*) as p from ' + QUERY_TABLE + ' where dirty is false and stopped = 0 and roadCategory is not null group by tid)f where ' + TABLE + '.tid=f.tid;'
#print s
con.query(s)

s = 'update ' + TABLE + '  set PSmallRoad = p from (select tid, count(case when roadCategory=3 then 1 end)::float/count(*) as p from ' + QUERY_TABLE + ' where dirty is false and stopped = 0 and roadCategory is not null group by tid)f where ' + TABLE + '.tid=f.tid;'
#print s
con.query(s)

#res = con.query('select speed, timestamp, tid  from ' + QUERY_TABLE + ' where tid in (select tid from ' + TABLE + ') and dirty is false order by tid, timestamp').getresult()


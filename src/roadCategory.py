import pg , math, sys, os ,time

USER = 'd103'
DB = "gps_can"
QUERY_TABLE = "a_gps_can_data"
MAP_TABLE = "osm_dk_20130214"
TABLE = "trip_data"



con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

con.query("alter table " + QUERY_TABLE + " drop IF EXISTS roadCategory;")
con.query('alter table ' + QUERY_TABLE + ' add roadCategory int;')


s = 'update ' + QUERY_TABLE + ' set roadCategory = (case when category in ( \'11\',\'12\')  then 1 when category in( \'13\',\'14\',\'15\',\'21\',\'31\') then 2 when category in (\'41\',\'42\',\'51\',\'63\') then 3 end) from ' + MAP_TABLE + ' where ' + MAP_TABLE + '.segmentkey=' + QUERY_TABLE + '.segmentkey;'
print s
con.query(s)


con.query("alter table " + TABLE + " drop IF EXISTS PMoterRoad;")
con.query('alter table ' + TABLE + ' add PMoterRoad int;')
con.query("alter table " + TABLE + " drop IF EXISTS PNormalRoad;")
con.query('alter table ' + TABLE + ' add PNormalRoad int;')
con.query("alter table " + TABLE + " drop IF EXISTS PSmallRoad;")
con.query('alter table ' + TABLE + ' add PSmallRoad int;')


s = 'update ' + TABLE + '  set PMoterRoad = p from (select tid, count(case when roadCategory=1 then 1 end)::float/count(*) as p from ' + QUERY_TABLE + ' where dirty is false group by tid)f where ' + TABLE + '.tid=f.tid;'
print s
con.query(s)

s = 'update ' + TABLE + '  set PNormalRoad = p from (select tid, count(case when roadCategory=2 then 1 end)::float/count(*) as p from ' + QUERY_TABLE + ' where dirty is false group by tid)f where ' + TABLE + '.tid=f.tid;'
print s
con.query(s)

s = 'update ' + TABLE + '  set PSmallRoad = p from (select tid, count(case when roadCategory=3 then 1 end)::float/count(*) as p from ' + QUERY_TABLE + ' where dirty is false group by tid)f where ' + TABLE + '.tid=f.tid;'
print s
con.query(s)

#res = con.query('select speed, timestamp, tid  from ' + QUERY_TABLE + ' where tid in (select tid from ' + TABLE + ') and dirty is false order by tid, timestamp').getresult()

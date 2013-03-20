import pg , math, sys, os ,time

USER = 'karsten'
DB = "gps_can"
QUERY_TABLE = "a_gps_can_data"
MAP_TABLE = "osm_dk_20130214"
TABLE = "trip_data"



con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

con.query("alter table " + QUERY_TABLE + " drop IF EXISTS roadCategory;")
con.query('alter table ' + QUERY_TABLE + ' add roadCategory int;')


s = 'explain update ' + QUERY_TABLE + ' set roadCategory = p from  (select (case when category in ( \'11\',\'12\')  then 1 when category in( \'13\',\'14\',\'15\',\'21\',\'31\') then 2 when category in (\'41\',\'42\',\'51\',\'63\') then 3 end) as p from ' + QUERY_TABLE + ' inner join ' + MAP_TABLE + ' on ' + MAP_TABLE + '.segmentkey=' + QUERY_TABLE + '.segmentkey)s;'
print s
con.query(s)


#res = con.query('select speed, timestamp, tid  from ' + QUERY_TABLE + ' where tid in (select tid from ' + TABLE + ') and dirty is false order by tid, timestamp').getresult()


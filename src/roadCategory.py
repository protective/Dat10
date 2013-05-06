import pg , math, sys, os ,time

USER = 'd103'
DB = "gps_can"


PREFIX = 'a'
if len(sys.argv) > 1:
	PREFIX = sys.argv[1]
QUERY_TABLE = ""+PREFIX+"_gps_can_data"
TABLE = ""+PREFIX+"_trip_data"

MAP_TABLE = "osm_dk_20130501"




con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

con.query("alter table " + QUERY_TABLE + " drop IF EXISTS roadCategory;")
con.query('alter table ' + QUERY_TABLE + ' add roadCategory int;')
print "begin update"



res = con.query("select segmentkey, (case when category in ( \'11\',\'12\')  then 1 when category in( \'13\',\'14\',\'15\',\'21\',\'22\',\'31\') then 2 when category in (\'32\',\'33\',\'41\',\'42\',\'51\',\'63\') then 3 end) from "+MAP_TABLE+";").getresult()
count = 0
for i in res:
	if(count%1000==0):
		print str(count) + "of " + str(len(res))
	count +=1
	if (i[1]):
		con.query("update "+PREFIX+"_gps_can_data set roadcategory = "+str(i[1]) + " where segmentkey = " + str(i[0]) + ";")



print "done update"
#con.query("create index "+MAP_TABLE+"_category_idx on "+MAP_TABLE+" (category);")


#s = 'update ' + QUERY_TABLE + ' set roadCategory = (case when category in ( \'11\',\'12\')  then 1 when category in( \'13\',\'14\',\'15\',\'21\',\'31\') then 2 when category in (\'41\',\'42\',\'51\',\'63\') then 3 end) from ' + MAP_TABLE + ' where ' + MAP_TABLE + '.segmentkey=' + QUERY_TABLE + '.segmentkey;'
#print s
#con.query(s)


con.query("alter table " + TABLE + " drop IF EXISTS PMoterRoad;")
con.query('alter table ' + TABLE + ' add PMoterRoad float not null default 0;')
con.query("alter table " + TABLE + " drop IF EXISTS PNormalRoad;")
con.query('alter table ' + TABLE + ' add PNormalRoad float not null default 0;')
con.query("alter table " + TABLE + " drop IF EXISTS PSmallRoad;")
con.query('alter table ' + TABLE + ' add PSmallRoad float not null default 0;')


con.query("alter table " + TABLE + " drop IF EXISTS MoterRoad;")
con.query('alter table ' + TABLE + ' add MoterRoad float not null default 0;')
con.query("alter table " + TABLE + " drop IF EXISTS NormalRoad;")
con.query('alter table ' + TABLE + ' add NormalRoad float not null default 0;')
con.query("alter table " + TABLE + " drop IF EXISTS SmallRoad;")
con.query('alter table ' + TABLE + ' add SmallRoad float not null default 0;')


s = 'update ' + TABLE + '  set MoterRoad = p from (select tid, count(case when roadCategory=1 then 1 end)::float as p from ' + QUERY_TABLE + ' where dirty is false and stopped = 0 and roadCategory is not null group by tid)f where ' + TABLE + '.tid=f.tid;'
#print s
con.query(s)

s = 'update ' + TABLE + '  set NormalRoad = p from (select tid, count(case when roadCategory=2 then 1 end)::float as p from ' + QUERY_TABLE + ' where dirty is false and stopped = 0 and roadCategory is not null group by tid)f where ' + TABLE + '.tid=f.tid;'
#print s
con.query(s)

s = 'update ' + TABLE + '  set SmallRoad = p from (select tid, count(case when roadCategory=3 then 1 end)::float as p from ' + QUERY_TABLE + ' where dirty is false and stopped = 0 and roadCategory is not null group by tid)f where ' + TABLE + '.tid=f.tid;'
#print s
con.query(s)


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


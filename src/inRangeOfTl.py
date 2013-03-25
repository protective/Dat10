import pg , math, sys, os ,time

USER = "d103"
DB = "gps_can"

PREFIX = 'a'
if len(sys.argv) > 1:
	PREFIX = sys.argv[1]
DATATABLE = ""+PREFIX+"_gps_can_data"
TRIPDATA = ""+PREFIX+"_trip_data"

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

res = con.query("select max(tid) from "+DATATABLE+"").getresult()
print res

for i in range(0,res[0][0]):
	con.query("update "+DATATABLE+" as "+PREFIX+" set tl = t.tlId from trafficlights as t where ST_Dwithin(t.geom,"+PREFIX+".geom,100) and "+PREFIX+".tid = "+ str(i) + ";")
	print str(i) + " of " + str(res[0][0]) 


#"update a_gps_can_data as a set tl = t.tlId from trafficlights as t where ST_Dwithin(t.geom,a.geom,100)"

#"explain update a_gps_can_data as a set tl = t.tlId from (select tlId from trafficlights where ST_Dwithin(geom,a.geom,100) )t"

print 'Percentage in idle wo_tl'
con.query('alter table ' + TRIPDATA + ' drop if exists idle_wo_tl_percentage;')
con.query('alter table ' + TRIPDATA + ' add idle_wo_tl_percentage float;')
con.query('update ' + TRIPDATA + ' set idle_wo_tl_percentage = p from (select tid, count(case when idle=1 and tl is null then 1 end)::float/count(*) as p from ' + DATATABLE + ' where dirty is false group by tid)f where ' + TRIPDATA + '.tid=f.tid;')

print 'Percentage in idle w_tl'
con.query('alter table ' + TRIPDATA + ' drop if exists idle_w_tl_percentage;')
con.query('alter table ' + TRIPDATA + ' add idle_w_tl_percentage float;')
con.query('update ' + TRIPDATA + ' set idle_w_tl_percentage = p from (select tid, count(case when idle=1 and tl is not null then 1 end)::float/count(*) as p from ' + DATATABLE + ' where dirty is false group by tid)f where ' + TRIPDATA + '.tid=f.tid;')


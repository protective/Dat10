import os, pg, math, sys, time

USER = 'd103'
DB = "gps_can"
DATATABLE = 'a_gps_can_data'
TRIPDATA = 'trip_data'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

print 'Percentate with cold engine'
con.query('alter table ' + TRIPDATA + ' drop if exists temperature_percentage;')
con.query('alter table ' + TRIPDATA + ' add temperature_percentage float;')
con.query('update ' + TRIPDATA + ' set temperature_percentage = p from (select tid, count(case when temperature < 70 and speed > 15 then 1 end)::float/count(*) as p from ' + DATATABLE + ' where dirty is false group by tid)f where ' + TRIPDATA +'.tid=f.tid;')

import random, time, math, pg, sys,os

USER = os.getlogin()
DB = 'gps_can'
TABLE = 'a_gps_can_data'
MIN_COUNT = 100

print "Setting dirty flag on " + TABLE
con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')
con.query('alter table ' + TABLE + ' add column dirty bool; update ' + TABLE + ' set dirty=false where tid in (select tid from (select tid, count(tid) from ' + TABLE + ' group by tid)a where a.count < ' + str(MIN_COUNT) + ');')

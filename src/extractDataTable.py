import pg, sys, os

OUTPUT = sys.argv[1]
TID = sys.argv[2]

USER = os.getlogin()
DB = 'gps_can'
TABLE = 'a_gps_can_data'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

con.query("drop table if exists " + OUTPUT + "; create table " + OUTPUT + " as (select extract('epoch' from age(timestamp, (select min(timestamp) from " + TABLE + " where tid=" + TID + "))), totalconsumed, speed, rpm, acceleration from " + TABLE + " where tid=" + TID + " order by timestamp);")
	

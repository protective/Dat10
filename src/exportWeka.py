import pg, sys, os, csv

USER = os.getlogin()
DB = 'gps_can'
TABLE = 'trip_data'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')
#
res = con.query("""select vehicleid, idle_percentage,idle_wo_tl_percentage,idle_w_tl_percentage, km_pr_l, acckm, acckmweight, stopngo, cruise_percentage, total_km, temperature_percentage, tlCounter/total_km, tlRedConter/total_km,tlGreenounter/total_km,

	(case 
		when km_pr_l < 4 then 'low' 
		when km_pr_l >= 4 and km_pr_l< 8 then 'medium'
		when km_pr_l >= 8 then 'high'
	end)
from """ + TABLE).getresult()

output = open('weka/' + TABLE + '.arff', 'wb')

output.write("""@RELATION iris
@ATTRIBUTE id	REAL
@ATTRIBUTE idle	REAL
@ATTRIBUTE idleWOTL	REAL
@ATTRIBUTE idleWTL	REAL
@ATTRIBUTE fuel	REAL
@ATTRIBUTE accel REAL
@ATTRIBUTE accelW REAL
@ATTRIBUTE stopngo REAL
@ATTRIBUTE cruise REAL
@ATTRIBUTE length REAL
@ATTRIBUTE temperature REAL
@ATTRIBUTE tlcounter REAL
@ATTRIBUTE tlRedCounter REAL
@ATTRIBUTE tlGreenCounter REAL
@ATTRIBUTE class	{low, medium, high}
@DATA
""")


spamwriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
for r in res:
	spamwriter.writerow(r)

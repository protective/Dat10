import pg, sys, os, csv

USER = os.getlogin()
DB = 'gps_can'
TABLE = 'trip_data'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')
#
<<<<<<< HEAD
res = con.query("""select vehicleid, idle_percentage, km_pr_l, acckm, stopngo, cruise_percentage, total_km, temperature_percentage,  
=======
res = con.query("""select vehicleid, idle_percentage, km_pr_l, acckm, acckmWeight, stopngo, cruise_percentage, total_km, 
>>>>>>> 674bfc2e2dc120153c3619195e276d820b5c71b6
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
@ATTRIBUTE fuel	REAL
@ATTRIBUTE accel REAL
@ATTRIBUTE accelW REAL
@ATTRIBUTE stopngo REAL
@ATTRIBUTE cruise REAL
@ATTRIBUTE length REAL
<<<<<<< HEAD
@ATTRIBUTE temperature REAL
@ATTRIBUTE class	{low, medium, high}
=======
@ATTRIBUTE class	{low, medium ,high}
>>>>>>> 674bfc2e2dc120153c3619195e276d820b5c71b6

@DATA
""")


spamwriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
for r in res:
	spamwriter.writerow(r)

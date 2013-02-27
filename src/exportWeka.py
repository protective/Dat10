import pg, sys, os, csv

USER = os.getlogin()
DB = 'gps_can'
TABLE = 'trip_data'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')
#
res = con.query("""select vehicleid, idle_percentage, km_pr_l, acckm, stopngo, cruise_percentage, total_km, 
	(case 
		when km_pr_l < 2 then 'verylow' 
		when km_pr_l >= 2 and km_pr_l< 8 then 'low'
		when km_pr_l >= 8 then 'veryhigh'
	end)
from """ + TABLE).getresult()

output = open('weka/' + TABLE + '.arff', 'wb')

output.write("""@RELATION iris
@ATTRIBUTE id	REAL
@ATTRIBUTE idle	REAL
@ATTRIBUTE fuel	REAL
@ATTRIBUTE accel REAL
@ATTRIBUTE stopngo REAL
@ATTRIBUTE cruise REAL
@ATTRIBUTE length REAL
@ATTRIBUTE class	{verylow, low, veryhigh}

@DATA
""")


spamwriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
for r in res:
	spamwriter.writerow(r)

import pg, sys, os, csv

USER = os.getlogin()
DB = 'gps_can'
TABLE = 'trip_data'

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')

res = con.query("""select vehicleid, idle_percentage, km_pr_l,
	(case 
		when km_pr_l < 6 then 'low' 
		when km_pr_l >= 6 and km_pr_l< 7 then 'medium'
		when km_pr_l >= 7 then 'high'
	end)
from """ + TABLE).getresult()

output = open('weka/' + TABLE + '.arff', 'wb')

output.write("""@RELATION iris
@ATTRIBUTE id	REAL
@ATTRIBUTE idle	REAL
@ATTRIBUTE fuel	REAL
@ATTRIBUTE class	{low, medium, high}

@DATA
""")


spamwriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
for r in res:
	spamwriter.writerow(r)

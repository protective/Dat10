import pg, sys, os, csv

USER = "d103"
DB = 'gps_can'


PREFIX = 'a'
if len(sys.argv) > 1:
	PREFIX = sys.argv[1]
TABLE = ""+PREFIX+"_trip_data"

con = pg.connect(dbname=DB, host='localhost', user=USER,passwd='F1ff')
#

clusters = []
clusters.append(con.query('select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+ TABLE + ';').getresult()[0][0])
clusters.append(con.query('select avg(km_pr_l) from '+TABLE+' where km_pr_l > (select avg(km_pr_l)-stddev_samp(km_pr_l) as s from '+TABLE+')').getresult()[0][0])

res = con.query("select vehicleid, idle_percentage, km_pr_l, stopngo, cruise_percentage,  tlCounter,PmoterRoad,PNormalRoad,PSmallRoad, (case when km_pr_l < "+ str(clusters[0]) + " then 'low' when km_pr_l >= "+ str(clusters[0]) + " and km_pr_l< "+ str(clusters[1]) + " then 'medium' when km_pr_l >= "+ str(clusters[1]) + " then 'high'	end)from " + TABLE).getresult()

output = open('weka/' + TABLE + '.arff', 'wb')

output.write("""@RELATION iris
@ATTRIBUTE id	REAL
@ATTRIBUTE idle	REAL
@ATTRIBUTE fuel	REAL
@ATTRIBUTE stopngo REAL
@ATTRIBUTE cruise REAL
@ATTRIBUTE tlcounter REAL
@ATTRIBUTE PmoterRoad REAL
@ATTRIBUTE PNormalRoad REAL
@ATTRIBUTE PSmallRoad REAL
@ATTRIBUTE class	{low, medium, high}
@DATA
""")


spamwriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
for r in res:
	spamwriter.writerow(r)

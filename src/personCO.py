import pg , math, sys

con = pg.connect(dbname='GPS_can', host='localhost', user='karsten',passwd='F1ff')

X = sys.argv[1]
Y = sys.argv[2]

print X
print Y
means = con.query('select avg('+ X +'),avg('+ Y +') from gps where vehicleid = 354330030804267').getresult()
means = means[0]
result = con.query('select '+ X +','+ Y +' from gps where vehicleid = 354330030804267').getresult()
sum1 = 0;
sum2 = 0;
sum3 = 0;


for r in result:
	if r[0] and r[1]:
		sum1 += (r[0]-means[0])*(r[1]-means[1])
		sum2 += (r[0]-means[0])**2
		sum3 += (r[1]-means[1])**2

final = sum1/(math.sqrt(sum2) * math.sqrt(sum3))


print final

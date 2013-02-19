import pg , math, sys

con = pg.connect(dbname='gps_can', host='localhost', user='karsten',passwd='F1ff')

X = sys.argv[1]
Y = sys.argv[2]

print X
print Y
means = con.query('select avg('+ X +'),avg('+ Y +') from a_gps_can_data where tid = 4606').getresult()
means = means[0]
result = con.query('select '+ X +','+ Y +' from a_gps_can_data where tid = 4606').getresult()
sum1 = 0;
sum2 = 0;
sum3 = 0;


for r in result:
	if r[0] and r[1]:
		sum1 += (float(r[0])-float(means[0]))*(float(r[1])-float(means[1]))
		sum2 += (float(r[0])-float(means[0]))**2
		sum3 += (float(r[1])-float(means[1]))**2

final = sum1/(math.sqrt(sum2) * math.sqrt(sum3))


print final

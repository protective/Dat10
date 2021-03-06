import os, pg , math, sys
import xml.parsers.expat



TL_TABLE = "trafficLights"
print "begin"
if len(sys.argv) > 1:
	print sys.argv[1]
	f = open(sys.argv[1])
else:
	print "ERROR To few arguments"
	
PREFIX = 'a'
if len(sys.argv) > 2:
	PREFIX = sys.argv[2]
TABLE = ""+PREFIX+"_gps_can_data"



con = pg.connect(dbname='gps_can', host='localhost', user='d103',passwd='F1ff')

con.query('drop table IF EXISTS ' + TL_TABLE + ';')
con.query('create table ' + TL_TABLE + ' (tlId bigint, lat REAL, lon REAL, geom geography(POINT,4326));')
tree = []

# 3 handler functions
def start_element(name, attrs):
	tree.append(attrs)
	if "k" in attrs:
		if attrs['k'] == "highway":
			if "v" in attrs:
				if attrs['v'] == "traffic_signals":
					#print attrs
					#print tree[-2]
					cur = "insert into " +TL_TABLE + " values("+tree[-2]["id"] +"," + tree[-2]["lat"] + "," + tree[-2]["lon"] + ");"
					#print cur					
					con.query(cur)
					
def end_element(name):
	tree.pop()
#def char_data(data):
    #print 'Character data:', repr(data)


p = xml.parsers.expat.ParserCreate()

p.StartElementHandler = start_element
p.EndElementHandler = end_element
#p.CharacterDataHandler = char_data


s = f.readline()
while(s):
	p.Parse(s)
	s = f.readline()

con.query("COMMIT;")
con.query("update "+ TL_TABLE +" set geom = ST_SetSRID(ST_MakePoint(lon,lat),4326);")
con.query("COMMIT;")
con.query("DROP INDEX IF EXISTS idx_"+TL_TABLE+" CASCADE; create index idx_"+TL_TABLE+" on "+TL_TABLE+" using gist(geom);")
con.query("COMMIT;")



print "DONE"









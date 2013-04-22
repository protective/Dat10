#!/bin/bash
DB=$1
PREFIX=$2
openstreet=false

echo "get trajectories"
python getTrajectories.py 120 0 30 $PREFIX

if ($openstreet) then
echo "load open streetmap"
psql -d $DB -f osm_dk_20130214.sql
psql -d $DB -c "create index osm_dk_20130214_segmentkey_idx on osm_dk_20130214 (segmentkey);"
psql -d $DB -c "create index osm_dk_20130214_category_idx on osm_dk_20130214 (category);"
fi

python tripData.py $PREFIX 
python adjustSpeed.py $PREFIX


screen -S idle -d -m python idle.py $PREFIX 250
screen -S tl -d -m sh -c "updatePostgis.sh $DB $PREFIX ; python inRangeOfTl.py 20 $PREFIX ; python extractTrafficLights.py maps/denmark.osm $PREFIX"
screen -S road -d -m python roadCategory.py $PREFIX
screen -S acc -d -m python acceleration.py $PREFIX
screen -S stopngo -d -m python stopngo.py $PREFIX
screen -S cruise -d -m python cruise.py 1 20 $PREFIX




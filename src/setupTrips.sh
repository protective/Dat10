#!/bin/bash
DB=$1
PREFIX=$2
TRIPTIME=$3
TRIPLENGTH=$4
mapmatch="nm"


getTrajectories=true
postgis=false
tripData=true
idle=true
cruise=true
trafficLights=true
acceleration=true
temperature=false


if ($getTrajectories) then
echo "get trajectories"
python getTrajectories.py $TRIPTIME 0 $TRIPLENGTH $PREFIX
fi


echo "Create geom postgis"
psql -d $DB -c "alter table "$PREFIX"_gps_can_data add column geom geography(POINT,4326);"
psql -d $DB -c "update "$PREFIX"_gps_can_data set geom = ST_SetSRID(ST_MakePoint(longitude,latitude),4326);"
psql -d $DB -c "DROP INDEX IF EXISTS idx_"$PREFIX"_gps_can_data_geom CASCADE; create index idx_"$PREFIX"_gps_can_data_geom on "$PREFIX"_gps_can_data using gist(geom);"
if ($postgis) then
echo "load open streetmap"
psql -d $DB -f osm_dk_20130214.sql
psql -d $DB -c "create index osm_dk_20130214_segmentkey_idx on osm_dk_20130214 (segmentkey);"
psql -d $DB -c "create index osm_dk_20130214_category_idx on osm_dk_20130214 (category);"
fi

if ($tripData) then
python tripData.py $PREFIX
fi

if ($idle) then
python idle.py $PREFIX 250 
fi

if ($cruise) then
python cruise.py 1 20 $PREFIX
fi

if ($trafficLights) then
python extractTrafficLights.py maps/denmark.osm $PREFIX
python inRangeOfTl.py 20 $PREFIX
fi

python roadCategory.py $PREFIX

if ($acceleration) then
python acceleration.py $PREFIX
python stopngo.py $PREFIX
fi

#if ($temperature) then
#python temperature.py $PREFIX
#fi



#!/bin/bash
DB=$1
PREFIX=$2
TRIPTIME=$3

getTrajectories=true
postgis=true
tripData=true
idle=true
cruise=true
trafficLights=true
acceleration=true
temperature=true


if ($getTrajectories) then
echo "get trajectories"
python getTrajectories.py $TRIPTIME 30 $PREFIX
fi

if ($postgis) then
echo "Create geom postgis"
psql -d $DB -c "alter table $PREFIX\_gps_can_data add column geom geography(POINT,4326);"
psql -d $DB -c "update $PREFIX\_gps_can_data set geom = ST_SetSRID(ST_MakePoint(longitude,latitude),4326);"

echo "load open streetmap"
psql -d $DB -f $2/osm_dk_20130214.sql

psql -d $DB -c "create create index osm_dk_20130214_segmentkey_idx on osm_dk_20130214 (segmentkey);"
psql -d $DB -c "create create index osm_dk_20130214_category_idx on osm_dk_20130214 (category);"
fi


if ($tripData) then
python tripData.py $PREFIX
fi

if ($idle) then
python idle.py 0 $PREFIX
fi

if ($cruise) then
python cruise.py $PREFIX
fi

if ($trafficLights) then
python extractTrafficLights.py maps/denmark.osm $PREFIX
python inRangeOfTl.py $PREFIX
fi

if ($acceleration) then
python noAcceleration.py $PREFIX
python noAccelerationW.py $PREFIX
python stopngo.py $PREFIX
fi

if ($temperature) then
python temperature.py $PREFIX
fi



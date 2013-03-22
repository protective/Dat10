#!/bin/bash
DB=$1
FILEPATH=$2
FILES=$FILEPATH/*.csv
TABLE='gps_can_data'

PREFIX='a'

resetDatabase=false
copyData=false
getTrajectories=false
postgis=false
indexes=false
tripData=false
idle=false
cruise=false
trafficLights=false
acceleration=false
temperature=false

if $resetDatabase then
psql -d template1 -c "drop database if exists $DB;"
psql -d template1 -c "create database $DB;"

psql -d $DB -c "Create EXTENSION postgis;"

psql -d $DB -c "drop table IF EXISTS $TABLE;"
psql -d $DB -c "create table $TABLE (vehicleid bigint, timestamp timestamp, longitude float, latitude float, speed float, compass int, satellites int, temperature float, rpm int, acceleration float, kmcounter float, fuellevel float, throttlepos float, totalconsumed float, actualconsumed float, actual_km_l float, make float, model int, capacity float, weight float, segmentkey int, direction varchar(8));"
fi

if $copyData then
echo "Copying data"
for f in $FILES
do
psql -d $DB -c "\copy $TABLE from '$f' DELIMITERS ';' CSV HEADER;"
echo "Done loading $f"
done
fi

if $getTrajectories then
echo "get trajectories"
python getTrajectories.py 20 30 a
fi

if $postgis then
echo "Create geom postgis"
psql -d $DB -c "alter table $PREFIX _gps_can_data add column geom geography(POINT,4326);"
psql -d $DB -c "update $PREFIX _gps_can_data set geom = ST_SetSRID(ST_MakePoint(longitude,latitude),4326);"

echo "load open streetmap"
psql -d $DB -f $2/osm_dk_20130214.sql

psql -d $DB -c "create create index osm_dk_20130214_segmentkey_idx on osm_dk_20130214 (segmentkey);"
psql -d $DB -c "create create index osm_dk_20130214_category_idx on osm_dk_20130214 (category);"
fi

if $indexes then
echo "Creating indexes"

psql -d $DB -c "DROP INDEX IF EXISTS vehid_idx CASCADE; create index vehid_idx on $TABLE (vehicleid)"
psql -d $DB -c "DROP INDEX IF EXISTS time_idx CASCADE; create index time_idx on $TABLE (timestamp)"
psql -d $DB -c "DROP INDEX IF EXISTS lng_idx CASCADE; create index lng_idx on $TABLE (longitude)"
psql -d $DB -c "DROP INDEX IF EXISTS lat_idx CASCADE; create index lat_idx on $TABLE (latitude)"
psql -d $DB -c "DROP INDEX IF EXISTS speed_idx CASCADE; create index speed_idx on $TABLE (speed)"
psql -d $DB -c "DROP INDEX IF EXISTS compass_idx CASCADE; create index compass_idx on $TABLE (compass)"
psql -d $DB -c "DROP INDEX IF EXISTS temperature_idx CASCADE; create index temperature_idx on $TABLE (temperature)"
psql -d $DB -c "DROP INDEX IF EXISTS rpm_idx CASCADE; create index rpm_idx on $TABLE (rpm)"
psql -d $DB -c "DROP INDEX IF EXISTS acc_idx CASCADE; create index acc_idx on $TABLE (acceleration)"
psql -d $DB -c "DROP INDEX IF EXISTS kmcounter_idx CASCADE; create index kmcounter_idx on $TABLE (kmcounter)"
psql -d $DB -c "DROP INDEX IF EXISTS totalconsumed_idx CASCADE; create index totalconsumed_idx on $TABLE (totalconsumed)"
psql -d $DB -c "DROP INDEX IF EXISTS segmentkey_idx CASCADE; create index segmentkey_idx on $TABLE (segmentkey)"
psql -d $DB -c "DROP INDEX IF EXISTS direction_idx CASCADE; create index direction_idx on $TABLE (direction)"

fi

if $tripData then
python tripData.py a
fi

if $idle then
python idle.py 0 a
fi

if $cruise then
python cruise.py a
fi

if $trafficLights then
python extractTrafficLights.py maps/denmark.osm a
python inRangeOfTl.py a
fi

if $acceleration then
python noAcceleration.py a
python noAccelerationW.py a
python stopngo.py a
fi

if $temperature then
python temperature.py a
fi























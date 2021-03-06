#!/bin/bash
DB=$1
FILEPATH=$2
TABLE=$3
FILES=$FILEPATH/*.csv

resetDatabase=false
loadGPSTable=false
loadMapTable=true
copyData=true

if $resetDatabase 
then
echo "Creating database"
psql -d template1 -c "drop database if exists $DB;"
psql -d template1 -c "create database $DB;"
psql -d $DB -c "Create EXTENSION postgis;"
fi

if $loadGPSTable 
then
echo "Creating $TABLE"
psql -d $DB -c "drop table IF EXISTS $TABLE;"
psql -d $DB -c "create table $TABLE (vehicleid bigint, timestamp timestamp, longitude float, latitude float, speed float, compass int, satellites int, temperature float, rpm int, acceleration float, kmcounter float, fuellevel float, throttlepos float, totalconsumed float, actualconsumed float, actual_km_l float, make float, model int, capacity float, weight float);"
fi

if $loadMapTable 
then
echo "Creating $TABLE"
psql -d $DB -c "drop table IF EXISTS $TABLE;"
psql -d $DB -c "create table $TABLE (vehicleid bigint, timestamp timestamp, longitude float, latitude float, speed float, compass int, satellites int, temperature float, rpm int, acceleration float, kmcounter float, fuellevel float, throttlepos float, totalconsumed float, actualconsumed float, actual_km_l float, make float, model int, capacity float, weight float, segmentkey int, direction varchar(8));"
fi

if $copyData 
then
echo "Copying data"
for f in $FILES
do
psql -d $DB -c "\copy $TABLE from '$f' DELIMITERS ';' CSV HEADER;"
echo "Done loading $f"
done
echo "Renaming"
psql -d $DB -c "update $TABLE set vehicleid=3 where vehicleid=354330030714458;"
psql -d $DB -c "update $TABLE set vehicleid=4 where vehicleid=354330030804267;"
psql -d $DB -c "update $TABLE set vehicleid=2 where vehicleid=354330030793940;"
psql -d $DB -c "update $TABLE set vehicleid=1 where vehicleid=354330030781010;"


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

if $loadMapTable 
then
psql -d $DB -c "DROP INDEX IF EXISTS segmentkey_idx CASCADE; create index segmentkey_idx on $TABLE (segmentkey)"
psql -d $DB -c "DROP INDEX IF EXISTS direction_idx CASCADE; create index direction_idx on $TABLE (direction)"
fi
fi
























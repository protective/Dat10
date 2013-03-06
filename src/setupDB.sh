#!/bin/bash
DB=$1
FILEPATH=$2
FILES=$FILEPATH/*.csv
TABLE='gps_can_data'
psql -d template1 -c "drop database if exists gps_can;"
psql -d template1 -c "create database gps_can;"

psql -d $DB -f 'psql -d gps_can -c "Create EXTENSION postgis;"'

psql -d $DB -c "drop table IF EXISTS $TABLE;"
psql -d $DB -c "create table $TABLE (vehicleid bigint, timestamp timestamp, longitude float, latitude float, speed float, direction int, satellites int, temperature float, rpm int, acceleration float, kmcounter float, fuellevel float, throttlepos float, totalconsumed float, actualconsumed float, actual_km_l float, make float, model int, capacity float, weight float);"

echo "Copying data"
for f in $FILES
do
psql -d $DB -c "\copy $TABLE from '$f' DELIMITERS ';' CSV HEADER;"
echo "Done loading $f"
done

echo "get trajectories"
python getTrajectories.py

echo "Create geom postgis"
psql -d $DB -c "alter table a_gps_can_data add column geom geography(POINT,4326);"
psql -d $DB -c "update a_gps_can_data set geom = ST_SetSRID(ST_MakePoint(longitude,latitude),4326);"

echo "Creating indexes"

psql -d $DB -c "DROP INDEX IF EXISTS idx_a_gps_can_data CASCADE; create index idx_a_gps_can_data on a_gps_can_data using gist(geom);"
psql -d $DB -c "DROP INDEX IF EXISTS vehid_idx CASCADE; create index vehid_idx on $TABLE (vehicleid)"
psql -d $DB -c "DROP INDEX IF EXISTS time_idx CASCADE; create index time_idx on $TABLE (timestamp)"
psql -d $DB -c "DROP INDEX IF EXISTS lng_idx CASCADE; create index lng_idx on $TABLE (longitude)"
psql -d $DB -c "DROP INDEX IF EXISTS lat_idx CASCADE; create index lat_idx on $TABLE (latitude)"
psql -d $DB -c "DROP INDEX IF EXISTS speed_idx CASCADE; create index speed_idx on $TABLE (speed)"
psql -d $DB -c "DROP INDEX IF EXISTS temperature_idx CASCADE; create index temperature_idx on $TABLE (temperature)"
psql -d $DB -c "DROP INDEX IF EXISTS rpm_idx CASCADE; create index rpm_idx on $TABLE (rpm)"
psql -d $DB -c "DROP INDEX IF EXISTS acc_idx CASCADE; create index acc_idx on $TABLE (acceleration)"
psql -d $DB -c "DROP INDEX IF EXISTS totalconsumed_idx CASCADE; create index totalconsumed_idx on $TABLE (totalconsumed)"

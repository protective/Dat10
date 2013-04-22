#!/bin/bash
DB=$1
PREFIX=$2

echo "Create geom postgis"
psql -d $DB -c "alter table "$PREFIX"_gps_can_data add column geom geography(POINT,4326);"
psql -d $DB -c "update "$PREFIX"_gps_can_data set geom = ST_SetSRID(ST_MakePoint(longitude,latitude),4326);"
psql -d $DB -c "DROP INDEX IF EXISTS idx_"$PREFIX"_gps_can_data_geom CASCADE; create index idx_"$PREFIX"_gps_can_data_geom on "$PREFIX"_gps_can_data using gist(geom);"

#!/bin/bash     
DB=$1
DBTB=$2
FIRST_COL=$3
FIRST_NAME=$4
SECOND_COL=$5
SECOND_NAME=$6
OUTPUT=$7

psql -d $DB -c "\copy $DBTB to '/home/sabrine/speciale/images/$OUTPUT"_"$FIRST_NAME$SECOND_NAME.csv' delimiter ' ' csv"

echo "set terminal png size 1000,500; set output '$OUTPUT"_"$FIRST_NAME$SECOND_NAME.png'; set y2tics; plot '$OUTPUT"_"$FIRST_NAME$SECOND_NAME.csv' using 1:$FIRST_COL with lines title '$FIRST_NAME', '$OUTPUT"_"$FIRST_NAME$SECOND_NAME.csv' using 1:$SECOND_COL with lines axes x1y2 title '$SECOND_NAME'" | gnuplot

#unset xtics;


if [ -z "$1" ]; then
	PREFIX="a"
else
	PREFIX=$1
fi
TRIPS=$PREFIX"_trip_data"
IDLEDATA=$PREFIX'_idledatatl'
CRUISEDATA=$PREFIX'_cruise_data'
GPSDATA=$PREFIX'_gps_can_data'

scp extractImages.py d103@172.25.26.191:Dat10/src/


if [ ! -d $PREFIX"_images" ]; then
    mkdir $PREFIX"_images"
fi

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trafficlight $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trafficlight.png $PREFIX"_images"/trafficlight.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trafficlightgreen $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trafficlightgreen.png $PREFIX"_images"/trafficlightgreen.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trafficlightred $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trafficlightred.png $PREFIX"_images"/trafficlightred.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trafficlightratio $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trafficlightratio.png $PREFIX"_images"/trafficlightratio.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py cruisep f_trip_data | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/cruisep.png $PREFIX"_images"/cruisep.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py moterRoad $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/moterRoad.png $PREFIX"_images"/moterRoad.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py smallRoad $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/smallRoad.png $PREFIX"_images"/smallRoad.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py normalRoad $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/normalRoad.png $PREFIX"_images"/normalRoad.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idle2 $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idle2.png $PREFIX"_images"/idle2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idle3 $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idle3.png $PREFIX"_images"/idle3.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py TripsKmlCluster $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TripsKmlCluster.png $PREFIX"_images"/TripsKmlCluster.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py cruiseSpeedKml $CRUISEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/cruiseSpeedKml.png $PREFIX"_images"/cruiseSpeedKml.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleRange2 $IDLEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleRange2.png $PREFIX"_images"/idleRange2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleRange22 $IDLEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleRange22.png $PREFIX"_images"/idleRange22.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py km_pr_l $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/kmlTrips.png $PREFIX"_images"/kmlTrips.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py steadySpeedExample $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/steadySpeedExample.png $PREFIX"_images"/steadySpeedExample.png




ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py cruiseCounter $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/cruiseCounter.png $PREFIX"_images"/cruiseCounter.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py testClusters | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/testClusters.png $PREFIX"_images"/testClusters.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationRanges $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationRanges.png $PREFIX"_images"/accelerationRanges.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationFast $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationFast.png $PREFIX"_images"/accelerationFast.png





ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py rpmRanges $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/rpmRanges.png $PREFIX"_images"/rpmRanges.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleRange3 $IDLEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleRange3.png $PREFIX"_images"/idleRange3.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleDuration $IDLEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleDuration.png $PREFIX"_images"/idleDuration.png





ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py LengthTrips $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TripsLength.png $PREFIX"_images"/TripsLength.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py LengthTrips2 $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TripsLength2.png $PREFIX"_images"/TripsLength2.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py TimeTrips $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TimeTrips.png $PREFIX"_images"/TimeTrips.png








ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py tlRange $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/tlRange.png images/tlRange.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py testRoad $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/testRoad.png $PREFIX"_images"/testRoad.png
: << 'COMMENT'
COMMENT




ssh -x -l d103 172.25.26.191 "cd Dat10/src/;git checkout extractImages.py"









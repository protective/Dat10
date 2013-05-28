
if [ -z "$1" ]; then
	PREFIX="a"
else
	PREFIX=$1
fi
TRIPS=$PREFIX"_trip_data"
IDLEDATA=$PREFIX'_idledatatl'
CRUISEDATA=$PREFIX'_cruise_data'
ACCDATA=$PREFIX'_accdata3'
ACC4DATA=$PREFIX'_accdata4'
GPSDATA=$PREFIX'_gps_can_data'

scp extractImages.py d103@172.25.26.191:Dat10/src/


if [ ! -d $PREFIX"_images" ]; then
    mkdir $PREFIX"_images"
fi

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py acceleration3D $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/100acceleration3D.png $PREFIX"_images"/100acceleration3D.png
scp d103@172.25.26.191:Dat10/src/images/101acceleration3D.png $PREFIX"_images"/101acceleration3D.png
scp d103@172.25.26.191:Dat10/src/images/0acceleration3D.png $PREFIX"_images"/0acceleration3D.png
scp d103@172.25.26.191:Dat10/src/images/1acceleration3D.png $PREFIX"_images"/1acceleration3D.png
scp d103@172.25.26.191:Dat10/src/images/2acceleration3D.png $PREFIX"_images"/2acceleration3D.png
scp d103@172.25.26.191:Dat10/src/images/3acceleration3D.png $PREFIX"_images"/3acceleration3D.png
scp d103@172.25.26.191:Dat10/src/images/4acceleration3D.png $PREFIX"_images"/4acceleration3D.png
: << 'COMMENT'

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationRanges2 $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationRanges2.png $PREFIX"_images"/accelerationRanges2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationRanges2a $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationRanges2a.png $PREFIX"_images"/accelerationRanges2a.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleRange2 $IDLEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleRange2.png $PREFIX"_images"/idleRange2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleRange22 $IDLEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleRange22.png $PREFIX"_images"/idleRange22.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleRange3 $IDLEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleRange3.png $PREFIX"_images"/idleRange3.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py km_pr_l $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/kmlTrips.png $PREFIX"_images"/kmlTrips.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py cruiseExample $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/cruiseExample.png $PREFIX"_images"/cruiseExample.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py compareVehicles2 $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/1Compare.png $PREFIX"_images"/1Compare.png
scp d103@172.25.26.191:Dat10/src/images/2Compare.png $PREFIX"_images"/2Compare.png
scp d103@172.25.26.191:Dat10/src/images/3Compare.png $PREFIX"_images"/3Compare.png
scp d103@172.25.26.191:Dat10/src/images/4Compare.png $PREFIX"_images"/4Compare.png







ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationCounter $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationCounter.png $PREFIX"_images"/accelerationCounter.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationFuelStart2 $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationFuelStart2.png $PREFIX"_images"/accelerationFuelStart2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationFuelStart2Data $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationFuelStart2Data.png $PREFIX"_images"/accelerationFuelStart2Data.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py moterRoad $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/moterRoad.png $PREFIX"_images"/moterRoad.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py smallRoad $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/smallRoad.png $PREFIX"_images"/smallRoad.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py normalRoad $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/normalRoad.png $PREFIX"_images"/normalRoad.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py checkFuel $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/checkFuel.png $PREFIX"_images"/checkFuel.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py song $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/song.png $PREFIX"_images"/song.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py songData $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/songData.png $PREFIX"_images"/songData.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py frequency $GPSDATA | gnuplot "
scp d103@172.25.26.191:Dat10/src/images/frequency.png $PREFIX"_images"/frequency.png




ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectoryTrafficLight $GPSDATA 1 | gnuplot  "
scp d103@172.25.26.191:Dat10/src/images/trajectoryTrafficLight.png $PREFIX"_images"/trajectoryTrafficLight1.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectoryTrafficLight $GPSDATA 2 | gnuplot  "
scp d103@172.25.26.191:Dat10/src/images/trajectoryTrafficLight.png $PREFIX"_images"/trajectoryTrafficLight2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectory $GPSDATA 1 | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trajectory.png $PREFIX"_images"/trajectory1.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectory $GPSDATA 2 | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trajectory.png $PREFIX"_images"/trajectory2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectory $GPSDATA 3 | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trajectory.png $PREFIX"_images"/trajectory3.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py speedlimitCount $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/speedlimitCount.png $PREFIX"_images"/speedlimitCount.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectoryFuleCost $GPSDATA| gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trajectoryFuleCost.png $PREFIX"_images"/trajectoryFuleCost.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py cruiseSpeedKml $CRUISEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/cruiseSpeedKml.png $PREFIX"_images"/cruiseSpeedKml.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py showClusters $TRIPS"

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py TripsKmlCluster $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TripsKmlCluster.png $PREFIX"_images"/TripsKmlCluster.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py tlRange $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/tlRange.png $PREFIX"_images"/tlRange.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py cruiseCounter $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/cruiseCounter.png $PREFIX"_images"/cruiseCounter.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trafficlight $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trafficlight.png $PREFIX"_images"/trafficlight.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py cruisep f_trip_data | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/cruisep.png $PREFIX"_images"/cruisep.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idle2 $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idle2.png $PREFIX"_images"/idle2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idle3 $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idle3.png $PREFIX"_images"/idle3.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py steadySpeedExample $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/steadySpeedExample.png $PREFIX"_images"/steadySpeedExample.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py rpmRanges $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/rpmRanges.png $PREFIX"_images"/rpmRanges.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleDuration $IDLEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleDuration.png $PREFIX"_images"/idleDuration.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py LengthTrips $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TripsLength.png $PREFIX"_images"/TripsLength.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py TimeTrips $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TimeTrips.png $PREFIX"_images"/TimeTrips.png

COMMENT




ssh -x -l d103 172.25.26.191 "cd Dat10/src/;git checkout extractImages.py"









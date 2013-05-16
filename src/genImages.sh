
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

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationRanges4 $ACC4DATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationRanges4.png $PREFIX"_images"/accelerationRanges4.png

: << 'COMMENT'

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationRanges3a $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationRanges3a $PREFIX"_images"/accelerationRanges3a
ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationRanges3b $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationRanges3b.png $PREFIX"_images"/accelerationRanges3b.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectory $GPSDATA 1 | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trajectory.png $PREFIX"_images"/trajectory1.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectory $GPSDATA 2 | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trajectory.png $PREFIX"_images"/trajectory2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectoryTrafficLight $GPSDATA 1 | gnuplot  "
scp d103@172.25.26.191:Dat10/src/images/trajectoryTrafficLight.png $PREFIX"_images"/trajectoryTrafficLight1.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectoryTrafficLight $GPSDATA 2 | gnuplot  "
scp d103@172.25.26.191:Dat10/src/images/trajectoryTrafficLight.png $PREFIX"_images"/trajectoryTrafficLight2.png




ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationTEST $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationTEST.png $PREFIX"_images"/accelerationTEST.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectoryTrafficLight $GPSDATA | gnuplot  "
scp d103@172.25.26.191:Dat10/src/images/trajectoryTrafficLight.png $PREFIX"_images"/trajectoryTrafficLight.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationSpeedFuel2 $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationSpeedFuel2.png $PREFIX"_images"/accelerationSpeedFuel2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationRanges2 $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationRanges2.png $PREFIX"_images"/accelerationRanges2.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationSpeedFuel $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationSpeedFuel.png $PREFIX"_images"/accelerationSpeedFuel.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationRanges $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationRanges.png $PREFIX"_images"/accelerationRanges.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationStddevAcc $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationStddevAcc.png $PREFIX"_images"/accelerationStddevAcc.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationFuelStart2 $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationFuelStart2.png $PREFIX"_images"/accelerationFuelStart2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationFuelStart2Data $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationFuelStart2Data.png $PREFIX"_images"/accelerationFuelStart2Data.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationFuelCounter $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationFuelCounter.png $PREFIX"_images"/accelerationFuelCounter.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationSpeed $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationSpeed.png $PREFIX"_images"/accelerationSpeed.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationSpeedFuelTime $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationSpeedFuelTime.png $PREFIX"_images"/accelerationSpeedFuelTime.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectory $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trajectory.png $PREFIX"_images"/trajectory.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectoryCruise $GPSDATA | gnuplot  "
scp d103@172.25.26.191:Dat10/src/images/trajectoryCruise.png $PREFIX"_images"/trajectoryCruise.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationSpeed $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationSpeed.png $PREFIX"_images"/accelerationSpeed.png



ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py compareVehicles $GPSDATA"
scp d103@172.25.26.191:Dat10/src/images/1Compare.png $PREFIX"_images"/1Compare.png
scp d103@172.25.26.191:Dat10/src/images/2Compare.png $PREFIX"_images"/2Compare.png
scp d103@172.25.26.191:Dat10/src/images/3Compare.png $PREFIX"_images"/3Compare.png
scp d103@172.25.26.191:Dat10/src/images/4Compare.png $PREFIX"_images"/4Compare.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleRange2 $IDLEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleRange2.png $PREFIX"_images"/idleRange2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleRange22 $IDLEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleRange22.png $PREFIX"_images"/idleRange22.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py speedlimitCount $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/speedlimitCount.png $PREFIX"_images"/speedlimitCount.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trajectoryFuleCost $GPSDATA| gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trajectoryFuleCost.png $PREFIX"_images"/trajectoryFuleCost.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py rpmAcceleration $GPSDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/rpmAcceleration.png $PREFIX"_images"/rpmAcceleration.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py cruiseSpeedKml $CRUISEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/cruiseSpeedKml.png $PREFIX"_images"/cruiseSpeedKml.png










ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py accelerationFuel2 $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/accelerationFuel2.png $PREFIX"_images"/accelerationFuel2.png







ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py showClusters $TRIPS"

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py TripsKmlCluster $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TripsKmlCluster.png $PREFIX"_images"/TripsKmlCluster.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py km_pr_l $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/kmlTrips.png $PREFIX"_images"/kmlTrips.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py acceleration2 $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/acceleration2.png $PREFIX"_images"/acceleration2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py acceleration3 $ACCDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/acceleration3.png $PREFIX"_images"/acceleration3.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py tlRange $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/tlRange.png $PREFIX"_images"/tlRange.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py cruiseCounter $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/cruiseCounter.png $PREFIX"_images"/cruiseCounter.png







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


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py steadySpeedExample $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/steadySpeedExample.png $PREFIX"_images"/steadySpeedExample.png


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py testClusters | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/testClusters.png $PREFIX"_images"/testClusters.png


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


ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py testRoad $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/testRoad.png $PREFIX"_images"/testRoad.png



COMMENT




ssh -x -l d103 172.25.26.191 "cd Dat10/src/;git checkout extractImages.py"









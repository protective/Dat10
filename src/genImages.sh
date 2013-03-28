
if [ -z "$1" ]; then
	PREFIX="a"
else
	PREFIX=$1
fi
TRIPS=$PREFIX"_trip_data"
VEHICLEDATA=$PREFIX'_vehicledata'

scp extractImages.py d103@172.25.26.191:Dat10/src/


if [ ! -d $PREFIX"_images" ]; then
    mkdir $PREFIX"_images"
fi

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idle2 $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idle2.png $PREFIX"_images"/idle2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idle3 $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idle3.png $PREFIX"_images"/idle3.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idlePercent $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idlePercent.png $PREFIX"_images"/idlePercent.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleTime $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleTime.png $PREFIX"_images"/idleTime.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleDuration $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleDuration.png $PREFIX"_images"/idleDuration.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py km_pr_l $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/kmlTrips.png $PREFIX"_images"/kmlTrips.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py LengthTrips $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TripsLength.png $PREFIX"_images"/TripsLength.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleRange2 $VEHICLEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleRange2.png $PREFIX"_images"/idleRange2.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py idleRange3 $VEHICLEDATA | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleRange3.png $PREFIX"_images"/idleRange3.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py TimeTrips $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TimeTrips.png $PREFIX"_images"/TimeTrips.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py normalRoad $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/normalRoad.png $PREFIX"_images"/normalRoad.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py smallRoad $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/smallRoad.png $PREFIX"_images"/smallRoad.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py moterRoad $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/moterRoad.png $PREFIX"_images"/moterRoad.png

ssh -x -l d103 172.25.26.191 "cd Dat10/src/;python extractImages.py trafficlight $TRIPS | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/trafficlight.png $PREFIX"_images"/trafficlight.png










ssh -x -l d103 172.25.26.191 "cd Dat10/src/;git checkout extractImages.py"









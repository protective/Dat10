
if [ -z "$1" ]; then
	TABLE="a_trip_data"
else
	TABLE=$1
fi
echo $TABLE
ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py idle2 $TABLE | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idle2.png images/idle2.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py idle3 $TABLE | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idle3.png images/idle3.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py idlePercent $TABLE | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idlePercent.png images/idlePercent.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py idleTime $TABLE | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleTime.png images/idleTime.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py idleDuration $TABLE | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleDuration.png images/idleDuration.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py km_pr_l $TABLE | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/kmlTrips.png images/kmlTrips.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py LengthTrips $TABLE | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TripsLength.png images/TripsLength.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py TimeTrips $TABLE | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TimeTrips.png images/TimeTrips.png


#ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py normalRoad | gnuplot"
#scp d103@172.25.26.191:Dat10/src/images/normalRoad.png images/normalRoad.png


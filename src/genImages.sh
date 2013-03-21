ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py idle2 | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idle2.png images/idle2.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py idle3 | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idle3.png images/idle3.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py idlePercent | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idlePercent.png images/idlePercent.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py idleTime | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleTime.png images/idleTime.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py idleDuration | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/idleDuration.png images/idleDuration.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py km_pr_l | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/kmlTrips.png images/kmlTrips.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py LengthTrips | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TripsLength.png images/TripsLength.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py TimeTrips | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TimeTrips.png images/TimeTrips.png

ssh -x -l d103 172.25.26.191 "python Dat10/src/extractImages.py TripsSize | gnuplot"
scp d103@172.25.26.191:Dat10/src/images/TripsSize.png images/TripsSize.png


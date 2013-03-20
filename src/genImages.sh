ssh -x -l d103 172.25.26.79 "python Dat10/src/extractImages.py idle2 | gnuplot"
scp d103@172.25.26.79:Dat10/src/images/idle2.png images/idle2.png

ssh -x -l d103 172.25.26.79 "python Dat10/src/extractImages.py idle_percentage | gnuplot"
scp d103@172.25.26.79:Dat10/src/images/idle_percentageTrips.png images/idle_percentageTrips.png

ssh -x -l d103 172.25.26.79 "python Dat10/src/extractImages.py idle_time | gnuplot"
scp d103@172.25.26.79:Dat10/src/images/idle_timeTrips.png images/idle_timeTrips.png

ssh -x -l d103 172.25.26.79 "python Dat10/src/extractImages.py idleDuration | gnuplot"
scp d103@172.25.26.79:Dat10/src/images/idleDuration.png images/idleDuration.png

ssh -x -l d103 172.25.26.79 "python Dat10/src/extractImages.py LengthTrips | gnuplot"
scp d103@172.25.26.79:Dat10/src/images/TripsLength.png images/TripsLength.png

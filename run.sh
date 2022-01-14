#!/bin/bash
for((c=1; c>=1; c++))
do
result=`ps aux | grep -i "thermo2.py" | grep -v "grep" | wc -l`
	if [ $result -ge 1 ]
   	then
        echo "script is running"
   	else
        echo "script is not running"
	./thermo2.py & 

fi
	

done

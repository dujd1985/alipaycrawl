#!/bin/bash  
  
#for i in $(seq 1 10) 
while true
do
python alitest2.py
sleep 600
echo $i
done

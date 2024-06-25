#!/bin/bash
cd /home/hadoop/Projects/Avia
dt=$(date +"%Y%m%d_%H%M")

list1="conf/iata_1.txt"
list2="conf/iata_2.txt"
list3="conf/iata_3.txt"

echo $(date +"%Y-%m-%d %H:%M:%S") "Started: $dt" >> logs/runs/run_${dt}.log

scripts/run.sh $list1 $dt & 
PID1=$!
echo $(date +"%Y-%m-%d %H:%M:%S") "Running: scripts/run.sh $list1" >> logs/runs/run_${dt}.log

scripts/run.sh $list2 $dt & 
PID2=$!
echo $(date +"%Y-%m-%d %H:%M:%S") "Running: scripts/run.sh $list2" >> logs/runs/run_${dt}.log

scripts/run.sh $list3 $dt &
PID3=$!
echo $(date +"%Y-%m-%d %H:%M:%S") "Running: scripts/run.sh $list3" >> logs/runs/run_${dt}.log

wait $PID1
wait $PID2
wait $PID3

cat files/data_*${dt}.txt > files/data/data_${dt}.txt
echo $(date +"%Y-%m-%d %H:%M:%S") "Running: cat files/data_*${dt}.txt > files/data/data_${dt}.txt" >> logs/runs/run_${dt}.log

rm files/data_*${dt}.txt
echo $(date +"%Y-%m-%d %H:%M:%S") "Running: rm files/data_*${dt}.txt" >> logs/runs/run_${dt}.log >> logs/runs/run_${dt}.log

echo $(date +"%Y-%m-%d %H:%M:%S") "Completed: $dt" >> logs/runs/run_${dt}.log
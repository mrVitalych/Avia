#!/bin/bash
cd /home/hadoop/Projects/Avia

list=$1
dt=$2

while read -r org dst; do
    python3 scripts/main.py $org $dst $dt & 
    PID1=$!
    echo $(date +"%Y-%m-%d %H:%M:%S") "Running: python3 scripts/main.py $org $dst $dt" >> logs/runs/run_${dt}.log

    python3 scripts/main.py $dst $org $dt &
    PID2=$!
    echo $(date +"%Y-%m-%d %H:%M:%S") "Running: python3 scripts/main.py $dst $org $dt" >> logs/runs/run_${dt}.log
    
    wait $PID1
    wait $PID2
done < $list
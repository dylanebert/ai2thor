#!/bin/bash
for i in {1..100}
do
    echo $i
    python3 random_forces.py $i
done
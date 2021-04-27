#!/bin/bash
for i in {0..10000}
do
    echo $i
    python3 random_forces.py $i
done
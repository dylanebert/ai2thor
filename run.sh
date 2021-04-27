#!/bin/bash
for i in {0..200}
do
    echo $i
    python3 random_forces.py $i
done
#!/bin/bash -e
string=$1
file="$string.txt"
for x in {1..10}
do
echo $string
echo $string >> $file
sleep 1
done


#!/bin/bash -e
if [[ -z "$1" ]];
then
string='alex'
else
    string=$1
fi
file="$string.txt"
for x in {1..100}
do
echo $string
echo $string >> $file
sleep 1
done


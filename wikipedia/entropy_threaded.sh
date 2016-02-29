#!/bin/bash

file_size=`ls -l $1 | awk '{print $5}'`
thread_count=$2
chunk_size=`echo $file_size / $thread_count | bc` 
echo $chunk_size

for i in `seq 1 $thread_count` ; do
    offset=`echo "$chunk_size * $(($i-1))" | bc`
    binwalk -E -L.05 -v -l $chunk_size -o $offset $1 &
done
wait

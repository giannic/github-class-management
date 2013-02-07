#!/bin/bash

for dir in $(ls | grep hw_); do
    (cd $dir; git pull)
done

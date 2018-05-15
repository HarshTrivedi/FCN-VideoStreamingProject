#!/usr/bin/env bash

sudo sysctl -w net.ipv4.ip_forward=1

#use mahimahi to setup bottleneck downlink
mm-link bottleneck bottleneck --meter-downlink -- ./start.sh

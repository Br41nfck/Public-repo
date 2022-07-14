#!/bin/bash
clear
echo "Weather"
echo -n "Enter city name (start with capital letter): "
read name
curl -4 wttr.in/$name

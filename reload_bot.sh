#!/bin/bash
echo "***********************************************************"
echo `date '+%d-%B-%Y_%H:%M:%S'` " - Starting procedure..."
sleep 1
echo `date '+%d-%B-%Y_%H:%M:%S'` " - killing screen..."
screen -X -S "Discord-Bot" kill
sleep 1
echo `date '+%d-%B-%Y_%H:%M:%S'` " - Starting bot..."
screen -S "Discord-Bot" -d -m python3 {path_to_dir}/Lypus_Bot/Lypus_Bot.py
sleep 5
echo `date '+%d-%B-%Y_%H:%M:%S'` " - End procedure"

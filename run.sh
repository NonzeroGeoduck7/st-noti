#!/bin/bash

echo Starting on `date`

source ~/miniconda3/bin/activate st-noti
cd ~/st-noti
python src/source.py > log/$(date '+%F-%H:%M').log
source ~/miniconda3/bin/deactivate

echo Finished on `date`

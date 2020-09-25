#!/bin/bash

echo Starting on `date`

source /path/to/miniconda3/bin/activate st-noti
python /path/to/st-noti/src/source.py > /path/to/st-noti/log/$(date '+%F-%H:%M').log
source /path/to/miniconda3/bin/deactivate

echo Finished on `date`

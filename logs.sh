#!/usr/bin/env bash
cat ~/Dropbox/Records/Tech/mb8611/mb8611.log | jq ".data.GetMotoStatusLogResponse.MotoStatusLogList" | ./logs.py $@

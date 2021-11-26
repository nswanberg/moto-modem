#!/usr/bin/env bash
cat ~/Dropbox/Records/Tech/mb8611/mb8611.log | jq -c '{ts: .ts, downstream: .data.GetMotoStatusDownstreamChannelInfoResponse.MotoConnDownstreamChannel, upstream: .data.GetMotoStatusUpstreamChannelInfoResponse.MotoConnUpstreamChannel}' | ./power.py $@


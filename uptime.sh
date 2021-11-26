#!/usr/bin/env bash
cat ~/Dropbox/Records/Tech/mb8611/mb8611.log | jq '{ts: .ts, uptime: .data.GetMotoStatusConnectionInfoResponse.MotoConnSystemUpTime}'


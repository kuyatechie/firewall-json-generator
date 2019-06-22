#!/bin/bash

ip_list='./mgmt_ip_list.txt'
csv_file='./Code_Assignment_fw_rule_input.csv'

mkdir -p ./output

while read line; do
    ip="$(grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' <<< "$line")"
    python3 generate.py --source $csv_file --filename ./output/$ip
done < $ip_list
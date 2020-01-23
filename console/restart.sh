#!/bin/bash

rm -rf CI5235_Logs
rm -rf evtx_logs
rm -rf __pycache__
cp -r ~/Downloads/evtx_logs ./
rm -rf evtx_logs/.DS_Store
echo "READY!"

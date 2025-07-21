#!/bin/bash
clear
echo '===== BLITZPROXY v1.0 – Operation Blitz ====='

python3 /app/proxy-GetRawFiles.py
python3 /app/proxy-CheckRawFiles.py
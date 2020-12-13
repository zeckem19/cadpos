#!/bin/bash

sudo apt update
sudo apt install python3
sudo apt install python3-pip
git clone https://github.com/zeckem19/cadpos.git
cd cadpos
pip3 install -r requirements.txt

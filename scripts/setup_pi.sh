#!/bin/bash

sudo apt update
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
sudo make install
rm -rf redis-stable.tar.gz
cd ~
sudo apt install python3
sudo apt install python3-pip
pip3 install redis

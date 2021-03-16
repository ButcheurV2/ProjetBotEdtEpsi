#!/bin/bash

# test si on est root
test=`whoami`
if [ $test != "root" ]; then
  echo "Lancer en root ou sous sudo"
  exit
fi

apt update

apt install python3

# Install pip

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python get-pip.py

# Install openSSH si pas déjà

# sudo apt install openssh-server

# Install chrome sur UBUNTU 20.04

wget-q-O-https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

sh-c'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

apt update

sudo apt install google-chrome-stable

# Install chromium chromedriver

sudo apt install chromium-chromedriver




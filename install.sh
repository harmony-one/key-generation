#!/bin/bash

OS=$(uname -s)
if [ "$OS" == "Linux" ]; then
   sudo apt install python3 python3-distutils python3-dev
fi
if [ "$OS" == "Darwin" ]; then
    if [[ $(command -v brew) == "" ]]; then
        echo "Installing Hombrew"
        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    fi
    export PATH="/usr/local/bin:/usr/local/opt/python/libexec/bin:$PATH"
    brew install python3
fi

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py
sudo pip install -r requirements.txt

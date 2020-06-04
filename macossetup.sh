#!/bin/sh

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew install pkg-config
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
pip install pyenchant wget requests htmlparser pyside2
curl -O http://ftp.gnu.org/gnu/wget/wget-1.16.3.tar.gz
tar -xzf wget-1.16.3.tar.gz
cd wget-1.16.3
./configure --with-ssl=openssl
make
sudo make install
cd .. && rm -rf wget*

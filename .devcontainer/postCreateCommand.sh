#!/bin/bash
echo "Fixing locale..."
sudo apt-get update && sudo apt-get install -y locales
sudo locale-gen en_US.UTF-8
sudo update-locale LANG=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=LC_ALL=en_US.UTF-8

echo "Installing TA-Lib from mounted archive..."

cd /tmp/ta-lib-0.6.4
#tar -xzf ta-lib-0.6.4-src.tar.gz
#cd /ta-lib-0.6.4
./configure --prefix=/usr
make
sudo make install


# Install tools specified in mise.toml
#
cd /workspaces/real-time-ml-system-cohort-4
mise trust
mise install
echo 'eval "$(/usr/local/bin/mise activate bash)"' >> ~/.bashrc
source ~/.bashrc

#!/bin/bash

# Install tools specified in mise.toml
mise trust
mise install
echo 'eval "$(/usr/local/bin/mise activate bash)"' >> ~/.bashrc

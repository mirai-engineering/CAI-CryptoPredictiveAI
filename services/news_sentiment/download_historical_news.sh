#!/bin/bash

# git clone the repo that has the historical news
git clone https://github.com/soheilrahsaz/cryptoNewsDataset.git

# uncompress the .rar file at cryptoNewsDataset/csvOutput/cryptopanic_news.rar
unar cryptoNewsDataset/csvOutput/cryptopanic_news.rar -o data/

# remove the git repo folder
rm -rf cryptoNewsDataset
#!/bin/bash

# This gets run ON the EC2 instance (NOT in the GitHub Actions runner)

cd /home/ec2-user/dice

git pull

git fetch -all
git switch aws-project

sudo systemctl restart diceapp
sudo systemctl status diceapp --no-pager -l
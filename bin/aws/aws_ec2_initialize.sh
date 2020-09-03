#!/bin/bash
#setup script
set -x
exec 1> >(sudo tee /var/log/instance-setup.log) 2>&1

apt-get update 2>&1 >/dev/null
DEBIAN_FRONTEND=noninteractive apt-get -yq --force-yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade 2>&1 >/dev/null
apt-get install -y -f --no-install-recommends gcc git libssl-dev libffi-dev python3-pip python3-dev python3-setuptools libxml2-dev libxml2 libxslt1.1 libxslt1-dev build-essential firefox xvfb python3-lxml

#download Anaconda
wget https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
#install Anaconda

su ubuntu bash -c "bash Anaconda3-2020.07-Linux-x86_64.sh -b"

#upgrade pip
su ubuntu bash -c "source /home/ubuntu/.profile; python3 -m pip install --user --upgrade pip"

#add Anaconda to path
echo 'PATH=/home/ubuntu/anaconda3/bin:$PATH' >> /home/ubuntu/.profile

#create main program directory
su ubuntu bash -c "mkdir /home/ubuntu/scripts"

#configure git
export HOME='/home/ubuntu/'
GIT_AUTHOR_NAME="Alexander Cohen"
GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
git config --global user.name "$GIT_AUTHOR_NAME"
GIT_AUTHOR_EMAIL="alex@capitolmuckraker.com"
GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
git config --global user.email "$GIT_AUTHOR_EMAIL"

wget https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-linux64.tar.gz
tar -xvzf geckodriver-v0.27.0-linux64.tar.gz
su ubuntu bash -c "source /home/ubuntu/.profile; conda create -y -n basicscraper python=3.7 ipython"
cp geckodriver /home/ubuntu/anaconda3/envs/basicscraper/bin/

export code_url='https://github.com/capitolmuckrakr/arlington_va_courts.git'
su ubuntu bash -c "source /home/ubuntu/.profile; source activate basicscraper; python3 -m pip install selenium pyvirtualdisplay; cd /home/ubuntu/scripts; git clone $code_url"
su ubuntu bash -c "source /home/ubuntu/.profile; conda init bash"

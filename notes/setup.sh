###### python
sudo apt update && sudo apt -y install software-properties-common build-essential
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt -y install python3.7 python3-venv python3.7-venv python3.7-dev
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && sudo python3.7 get-pip.py \
    && rm get-pip.py

# sudo pip3.7 install --ignore-installed PyYAML
# sudo pip3.7 install pipenv httpie aws_okta_keyman awscli
# sudo pipenv shell
# sudo pipenv install --dev

###### nvm
# check version
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.0/install.sh | bash

# source ~/.bashrc
# nvm install v10.16.3
# nvm use v10.16.3

# nvm install v12.18.0
# nvm use v12.18.0

# nvm list # list installed versions
# nvm ls-remote # list all available versions

nvm alias default 12.18.0

# npm install -g serverless
# serverless upgrade

###### docker
sudo apt-get remove docker docker-engine docker.io containerd runc

sudo apt-get update 

sudo apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
	
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io

sudo usermod -aG docker $USER

# check version
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" \
	-o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "export DOCKER_HOST=tcp://localhost:2375" >> ~/.bashrc && source ~/.bashrc

###### ConEmu
SSH
ssh jaehyeon@172.28.175.19

PowerShell
-new_console:d:C:\Users\jakim\projects powershell.exe

WSL
powershell.exe bash

###### ssh key
ssh-keygen -t rsa -b 4096 -C "user@example.com"
ssh-keygen -f ./id_rsa -t rsa -b 4096 -C "comment"

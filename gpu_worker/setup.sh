# Install python3.10 and pip
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev python3-pip -y
python3 --version
ls -la /usr/bin/python3
sudo rm /usr/bin/python3
sudo ln -s python3.10 /usr/bin/python3
python3 --version

# Install ffmpeg

sudo apt install  -y ffmpeg

# Create virtual environment
python3 -m venv venv
source venv/bin/activate


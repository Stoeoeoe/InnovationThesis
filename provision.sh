set -e

mkdir -p /vagrant/app/{libs,temp}
mkdir /vagrant/app/libs/dragnet3

sudo apt-get update 

# Install git
sudo apt-get -y install git
sudo apt-get install -y curl
sudo apt-get install make

sudo apt-get -y install libatlas-base-dev libatlas-dev lib{blas,lapack}-dev
sudo apt-get -y install libxslt-dev libxml2-dev gcc g++

# Download and install Miniconda
cd /vagrant/app/temp
curl -O https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
bash Miniconda2-latest-Linux-x86_64.sh -b
rm Miniconda2-latest-Linux-x86_64.sh
	
# Create a Python 2.7 environment
export PATH=$HOME/miniconda2/bin:$PATH
conda_deps='pip numpy scipy'
conda create -m -p $HOME/py --yes $conda_deps python=2.7
export PATH=$HOME/py/bin:$PATH

# configure conda for future login (for vagrant)
echo "export PATH=$PATH" >> $HOME/.bashrc


# Install dragnet
touch ~/.ssh/config
cat <<EOT>> ~/.ssh/config
Host github.com
    StrictHostKeyChecking no
EOT

cd /vagrant/app/libs/dragnet3
git clone https://github.com/Stoeoeoe/dragnet.git

source activate /home/vagrant/py													# Use conda python
sudo pip install cython
sudo pip install numpy
cd /vagrant/app/libs/dragnet3/dragnet

sudo pip install -r requirements.txt    
sudo make install
make test
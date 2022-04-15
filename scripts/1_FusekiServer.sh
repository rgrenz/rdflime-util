#bin/bash

#
# Script to initialize and run an Apache Jena Fuseki server to offer our DBpedia data as SPARQL interface
#

sudo apt update -y
sudo apt install openjdk-11-jre gzip jq git wget unzip tmux bzip2 -y

# Get Jena & Fuseki
wget https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-4.4.0.zip -q --show-progress
wget https://dlcdn.apache.org/jena/binaries/apache-jena-4.4.0.zip -q --show-progress
unzip apache-jena-fuseki-4.4.0.zip
unzip apache-jena-4.4.0.zip
rm *.zip

# Get dbpedia
git clone https://github.com/rgrenz/lime
./lime/rdflime/data/download.sh

# Import dbpedia
# apache-jena-4.4.0/bin/tdb2.xloader --loc apache-jena-fuseki-4.4.0/run/datasets/dbpedia --threads=3 lime/rdflime/data/dbpedia/allData.nt
apache-jena-4.4.0/bin/tdb2.tdbloader --loc apache-jena-fuseki-4.4.0/run/datasets/dbpedia lime/rdflime/data/dbpedia/allData.nt

echo "Import is done."
echo "Run fuseki with the following command: apache-jena-fuseki-4.4.0/fuseki-server --loc apache-jena-fuseki-4.4.0/run/datasets/dbpedia /dbpedia"
echo "Try with sudo if it throws cryptic errors (especially on WSL)."
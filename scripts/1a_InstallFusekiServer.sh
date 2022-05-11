#bin/bash
set -e

#
# Script to initialize and run an Apache Jena Fuseki server to offer our DBpedia data as SPARQL interface
#

scriptsRoot=$(dirname "${BASH_SOURCE[0]}")
rdflimeUtil=$scriptsRoot/..

sudo apt update -y
sudo apt install openjdk-11-jre gzip jq git wget unzip tmux bzip2 -y

# Get Jena & Fuseki
mkdir $rdflimeUtil/jena
cd $rdflimeUtil/jena
wget https://archive.apache.org/dist/jena/binaries/apache-jena-4.4.0.zip --show-progress
wget https://archive.apache.org/dist/jena/binaries/apache-jena-fuseki-4.4.0.zip --show-progress
unzip apache-jena-fuseki-4.4.0.zip
unzip apache-jena-4.4.0.zip
rm *.zip

# Get dbpedia
if [ -d "$rdflimeUtil/data/dbpedia" ]; then
    echo "dbpedia folder already exists; skipping download."
else
    echo "Downloading dbpedia files and test datasets"
    $rdflimeUtil/data/download.sh
fi

# Import dbpedia
# apache-jena-4.4.0/bin/tdb2.xloader --loc apache-jena-fuseki-4.4.0/run/datasets/dbpedia --threads=3 lime/rdflime/data/dbpedia/allData.nt
$rdflimeUtil/jena/apache-jena-4.4.0/bin/tdb2.tdbloader --loc $rdflimeUtil/jena/apache-jena-fuseki-4.4.0/run/datasets/dbpedia $rdflimeUtil/data/dbpedia/allData.nt
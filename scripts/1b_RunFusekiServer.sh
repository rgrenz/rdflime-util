#bin/bash
set -e

scriptsRoot=$(dirname "${BASH_SOURCE[0]}")
rdflimeUtil=$scriptsRoot/..

echo "Running Apache Jena Fuseki server. You may want to forward port 3030 in case you are in a docker environment."

# Without sudo it sometimes throws cryptic erros
cd $rdflimeUtil/jena/apache-jena-fuseki-4.4.0
sudo ./fuseki-server --loc ./run/datasets/dbpedia /dbpedia
## rdflime-util
A collection of scripts and notebooks to replicate the results that have been reported in the corresponding thesis:<br>
__RDF-LIME: Locally Faithful Model-Agnostic Explanations for Machine Learning on Knowledge Graph Embeddings__

> In case you just want to use the RDF-LIME extension of the LIME library, please refer to [rdflime-core](https://github.com/rgrenz/rdflime-core).

### Replicating the results

#### Prerequisites
Ideally, start from a clean Linux system with Python 3 installed, e.g. using a fresh Python 3 docker image in the VS Code devcontainer environment.

__1. Download__ this repository:
```bash
git clone https://github.com/rgrenz/rdflime-util
```

__2. Basics__ To install and initiate Poetry, a python package manger, execute the following script:
```bash
./rdflime-util/scripts/0_PythonEnvironment.sh
```
__3. Fuseki__ We would like to generate knowledge graph embeddings from a DBpedia data dump. To achieve this, we first need to download the respective DBpedia triples and host them in Apache Jena Fuseki. Additionally, we will get the datasets for our entities of interest (e.g. movies).
```bash
# To download and setup Fuseki (one-time script)
./rdflime-util/scripts/1a_InstallFusekiServer.sh

# Every time you would then like to start Fuseki
./rdflime-util/scripts/1b_RunFusekiServer.sh

# You should then be able to access the Fuseki UI at http://localhost:3030
```

#### Embedding Generation
Now that Jena Fuseki is up and running, we can generate our graph embeddings using PyRDF2Vec. Depending on your editor, it could be useful to have a notebook extension installed. Make sure to choose the virtualenv that has been created by Poetry.

__1. Data Preprocessing__:
```bash
# (Optional) To have a first look into our datasets, you can play around in the following notebook:
./rdflime-util/notebooks/0_MovieDatasetExploration.ipynb

# Preprocessing - to correct some minor dataset errors, please run the cells in:
./rdflime-util/notebooks/1_DBpediaFixes.ipynb
```

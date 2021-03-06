#!/bin/bash
set -e

BLUE='\033[0;34m'
NC='\033[0m'
dataRoot=$(dirname "${BASH_SOURCE[0]}")
dbpediaSHA1=4127b5d0eb6ecc45350e7f0c619b3b6b88c3c24c

datasets=(
    metacritic-movies
    metacritic-albums
    forbes-companies
    mercer-cities
    aaup-universities
)

locations=(
    https://raw.githubusercontent.com/mariaangelapellegrino/Evaluation-Framework/master/evaluation_framework/Classification/data/MetacriticMovies.tsv
    https://raw.githubusercontent.com/mariaangelapellegrino/Evaluation-Framework/master/evaluation_framework/Classification/data/MetacriticAlbums.tsv
    https://raw.githubusercontent.com/mariaangelapellegrino/Evaluation-Framework/master/evaluation_framework/Classification/data/Forbes.tsv
    https://raw.githubusercontent.com/mariaangelapellegrino/Evaluation-Framework/master/evaluation_framework/Classification/data/Cities.tsv
    https://raw.githubusercontent.com/mariaangelapellegrino/Evaluation-Framework/master/evaluation_framework/Classification/data/AAUP.tsv 
)

# Download gold-standard datasets
for i in "${!datasets[@]}"; do
    dataset=${datasets[$i]}
    location=${locations[$i]}
    printf "✨ ${BLUE}Downloading ${dataset} dataset...${NC}\n"
    dataPath=$dataRoot/$dataset
    mkdir -p $dataPath
    wget $location -O $dataPath/data.tsv -q --show-progress
done

# Download dbpedia
printf "\n✨ ${BLUE}Downloading dbpedia...${NC}\n"
dbpediaPath=$dataRoot/dbpedia
rm -rf $dbpediaPath
dbpediaFragments=(
    http://downloads.dbpedia.org/2016-04/core/article_categories_en.ttl.bz2
    http://downloads.dbpedia.org/2016-04/core/instance_types_en.ttl.bz2
    http://downloads.dbpedia.org/2016-04/core/instance_types_transitive_en.ttl.bz2
    http://downloads.dbpedia.org/2016-04/core/mappingbased_objects_en.ttl.bz2
    http://downloads.dbpedia.org/2016-04/core/skos_categories_en.ttl.bz2
)
for fragment in ${dbpediaFragments[*]}
do
    wget $fragment -P $dbpediaPath -q --show-progress -nc --timeout=3
    sleep 1
done

# Unzip dbpedia fragments
printf "\n✨ ${BLUE}Unzipping dbpedia fragments (this may take a while)...${NC}\n"
for file in $dbpediaPath/*.bz2
do 
    echo $file
    bzip2 -d $file
done

# Concatenate
printf "\n✨ ${BLUE}Concatenating dbpedia fragments...${NC}\n"
for file in $dbpediaPath/*.ttl
do 
    echo $file
    cat $file >> $dbpediaPath/allData.nt
done

# Check SHA1 sum
printf "\n✨ ${BLUE}Checking dbpedia sha1sum...${NC}\n"
echo $dbpediaSHA1 $dbpediaPath/allData.nt > $dbpediaPath/allData.nt.sha1
sha1sum -c $dbpediaPath/allData.nt.sha1
if [ $? -gt 0 ]
then
    printf "❌ Checksum did not match!\nCheck https://github.com/mariaangelapellegrino/Evaluation-Framework#dataset-to-generate-embeddings\n"
    exit 1
else
    printf "✔️ Checksum matched!\n"
fi

# Cleanup
printf "\n✨ ${BLUE}Removing temporary dbpedia files...${NC}\n"
rm $dbpediaPath/*.ttl $dbpediaPath/*.sha1
echo "Done!"
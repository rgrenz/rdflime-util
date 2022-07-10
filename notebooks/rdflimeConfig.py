import pandas as pd
import os

dbpediaLocation = "http://localhost:3030/dbpedia"
dataLocation = "../data"
randomSeed = 42

datasets = [
    {
        "name": "metacritic-movies",
        "entity": "movies",
        "location": "../data/metacritic-movies",
        "columns": {
            "uri": "DBpedia_URI",
            "uri_fixed": "DBpedia_URI16",
            "uri_geval": "DBpedia_URI15",
            "label": "label",
            "rating": "rating"
        },
        "train_partition": [0, 1800],
        "test_partition": [1800, 2000],
        "active": True
    },
    {
        "name": "metacritic-albums",
        "entity": "albums",
        "location": "../data/metacritic-albums",
        "columns": {
            "uri": "DBpedia_URI",
            "uri_fixed": "DBpedia_URI16",
            "uri_geval": "DBpedia_URI15",
            "label": "label",
            "rating": "rating"
        },
        "train_partition": [0, 1440],
        "test_partition": [1440, 1600],
        "active": True
    },
    {
        "name": "forbes-companies",
        "entity": "companies",
        "location": "../data/forbes-companies",
        "columns": {
            "uri": "DBpedia_URI",
            "uri_fixed": "DBpedia_URI16",
            "uri_geval": "DBpedia_URI15",
            "label": "label",
            "rating": "rating"
        },
        "train_partition": [0, 1426],
        "test_partition": [1426, 1585],
        "active": True
    },
    {
        "name": "mercer-cities",
        "entity": "cities",
        "location": "../data/mercer-cities",
        "columns": {
            "uri": "DBpedia_URI",
            "uri_fixed": "DBpedia_URI16",
            "uri_geval": "DBpedia_URI15",
            "label": "label",
            "rating": "rating"
        },
        "train_partition": [0, 190],
        "test_partition": [190, 212],
        "active": True
    },
    {
        "name": "aaup-universities",
        "entity": "universities",
        "location": "../data/aaup-universities",
        "columns": {
            "uri": "DBpedia_URI",
            "uri_fixed": "DBpedia_URI16",
            "uri_geval": "DBpedia_URI15",
            "label": "label",
            "rating": "rating"
        },
        "train_partition": [0, 864],
        "test_partition": [864, 960],
        "active": True
    },
]
datasets = list(filter(lambda d: d["active"], datasets))


def load_dataset(cfg, fixed=True):
    file = "data_fixed.tsv" if fixed else "data.tsv"
    datasetFull = pd.read_csv(os.path.join(
        cfg["location"], file), sep="\t")
    uri_col = cfg["columns"]["uri_fixed"] if fixed else cfg["columns"]["uri"]
    datasetEntities = list(dict.fromkeys(
        [row[uri_col] for _, row in datasetFull.iterrows()]))  # Remove duplicates, keep order
    return (datasetFull, datasetEntities)


def split_dataset(dataset, cfg, randomize=True):
    if randomize:
        target = dataset.sample(frac=1, random_state=randomSeed)
    else:
        target = dataset
    train = target[cfg["train_partition"][0]:cfg["train_partition"][1]]
    test = target[cfg["test_partition"][0]:cfg["test_partition"][1]]
    return (train, test)

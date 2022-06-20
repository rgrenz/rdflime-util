import pandas as pd
import os

dbpediaLocation = "http://localhost:3030/dbpedia"

datasets = [
    {
        "name": "metacritic-movies",
        "location": "../data/metacritic-movies",
        "file": "movies_fixed.tsv",
        "columns": {
            "uri": "DBpedia_URI",
            "label": "label"
        },
        "train_partition": [400, 2000],
        "test_partition": [0, 400],
        "active": True
    },
    {
        "name": "metacritic-albums",
        "location": "../data/metacritic-albums",
        "file": "albums_fixed.tsv",
        "columns": {
            "uri": "DBpedia_URI",
            "label": "label"
        },
        "train_partition": [400, 2000],
        "test_partition": [0, 400],
        "active": True
    },
    {
        "name": "forbes-companies",
        "location": "../data/forbes-companies",
        "file": "movies_fixed.tsv",
        "columns": {
            "uri": "DBpedia_URI",
            "label": "label"
        },
        "train_partition": [400, 2000],
        "test_partition": [0, 400],
        "active": True
    }
]
datasets = list(filter(lambda d: d["active"], datasets))


def load_dataset(cfg):
    datasetFull = pd.read_csv(os.path.join(
        cfg["location"], cfg["file"]), sep="\t")
    uri_col = cfg["columns"]["uri"]
    datasetEntities = [row[uri_col] for _, row in datasetFull.iterrows()]
    return (datasetFull, datasetEntities)


def split_dataset(dataset, cfg):
    train = dataset[cfg["train_partition"][0]:cfg["train_partition"][1]]
    test = dataset[cfg["test_partition"][0]:cfg["test_partition"][1]]
    return (train, test)

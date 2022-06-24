import pandas as pd
import os

dbpediaLocation = "http://localhost:3030/dbpedia"

datasets = [
    {
        "name": "metacritic-movies",
        "entity": "movies",
        "location": "../data/metacritic-movies",
        "columns": {
            "uri": "DBpedia_URI",
            "label": "label",
            "rating": "rating"
        },
        "train_partition": [400, 2000],
        "test_partition": [0, 400],
        "active": True
    },
    {
        "name": "metacritic-albums",
        "entity": "albums",
        "location": "../data/metacritic-albums",
        "columns": {
            "uri": "DBpedia_URI",
            "label": "label",
            "rating": "rating"
        },
        "train_partition": [400, 2000],
        "test_partition": [0, 400],
        "active": True
    },
    {
        "name": "forbes-companies",
        "entity": "companies",
        "location": "../data/forbes-companies",
        "columns": {
            "uri": "DBpedia_URI",
            "label": "label",
            "rating": "rating"
        },
        "train_partition": [400, 2000],
        "test_partition": [0, 400],
        "active": True
    },
    {
        "name": "mercer-cities",
        "entity": "cities",
        "location": "../data/mercer-cities",
        "columns": {
            "uri": "DBpedia_URI",
            "label": "label",
            "rating": "rating"
        },
        "train_partition": [400, 2000],
        "test_partition": [0, 400],
        "active": True
    },
    {
        "name": "aaup-salaries",
        "entity": "salaries",
        "location": "../data/aaup-salaries",
        "columns": {
            "uri": "DBpedia_URI",
            "label": "label",
            "rating": "rating"
        },
        "train_partition": [400, 2000],
        "test_partition": [0, 400],
        "active": True
    },
]
datasets = list(filter(lambda d: d["active"], datasets))


def load_dataset(cfg, fixed=True):
    file = "data_fixed.tsv" if fixed else "data.tsv"
    datasetFull = pd.read_csv(os.path.join(
        cfg["location"], file), sep="\t")
    uri_col = cfg["columns"]["uri"]
    datasetEntities = [row[uri_col] for _, row in datasetFull.iterrows()]
    return (datasetFull, datasetEntities)


def split_dataset(dataset, cfg):
    train = dataset[cfg["train_partition"][0]:cfg["train_partition"][1]]
    test = dataset[cfg["test_partition"][0]:cfg["test_partition"][1]]
    return (train, test)

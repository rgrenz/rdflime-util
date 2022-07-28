import pandas as pd
import os.path
import pickle
import json
from pathlib import Path
from pyrdf2vec import RDF2VecTransformer
from pyrdf2vec.embedders import Word2Vec
from pyrdf2vec.graphs import KG
from pyrdf2vec.walkers import RandomWalker
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from evaluation_framework.manager import FrameworkManager
from rdflimeConfig import (
    dbpediaLocation,
    dataLocation,
    datasets,
    load_dataset,
    split_dataset,
)

for cfg in datasets:
    for algo in [0, 1]:  # 0: CBOW, 1: SG
        for vsize in [50, 100, 200]:  # Vector size of embeddings
            print(cfg["name"], algo, vsize)

            dataset, entities = load_dataset(cfg)
            datasetLocation = cfg["location"]

            targetPath = os.path.join(datasetLocation, "transformers")
            targetFile = f"rdf2vec_transformer_{'sg' if algo else 'cbow'}_{vsize}"
            if os.path.exists(os.path.join(targetPath, targetFile)):
                print(f"Skipping transformer, as it already exists.")
                continue

            dbpedia = KG(dbpediaLocation, skip_verify=False, mul_req=False)

            transformer = RDF2VecTransformer(
                Word2Vec(sg=algo, vector_size=vsize),  # negative = 25
                walkers=[
                    RandomWalker(
                        max_walks=500,
                        max_depth=4,
                        with_reverse=False,
                        n_jobs=2,
                        md5_bytes=None,
                    )
                ],  # max_walks = 22, max_depth = 2
                verbose=1,
            )

            walks = transformer.get_walks(dbpedia, entities)
            transformer.fit(walks)
            embeddings, literals = transformer.transform(dbpedia, entities)

            Path(targetPath).mkdir(parents=True, exist_ok=True)
            transformer.save(os.path.join(targetPath, targetFile))

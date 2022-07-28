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
from rdflimeConfig import dbpediaLocation, dataLocation, datasets, load_dataset, split_dataset

for cfg in datasets:
    datasetLocation = cfg["location"]
    dataset, entities = load_dataset(cfg)

    for algo in ["cbow", "sg"]:
        for vsize in [50, 100, 200]: # Vector size of embeddings

            with open(os.path.join(datasetLocation, "transformers", f"rdf2vec_transformer_{algo}_{vsize}"), "rb") as file:
                transformer: RDF2VecTransformer = pickle.load(file)

            targetPath = os.path.join(dataLocation, "embeddings")
            Path(targetPath).mkdir(parents=True, exist_ok=True)

            with open(os.path.join(targetPath, f"embeddings_{algo}_{vsize}"), "a") as file:
                for entity, embedding in zip(transformer._entities, transformer._embeddings):

                    # "Unfix" IRI and replace with the version that the Evaluation Framework by Pellegrino et al. understands
                    entity = dataset[dataset[cfg["columns"]["uri_fixed"]] == entity][cfg["columns"]["uri_geval"]].iloc[0].replace(" ", "+")        

                    # Write embedding to file
                    line = f"{entity} {' '.join(map(str,embedding))}\n"
                    file.write(line)
                    
evalPath = os.path.join(dataLocation, "embeddings", "evaluation")
Path(evalPath).mkdir(parents=True, exist_ok=True)

for algo in ["cbow", "sg"]:
    for vsize in [50, 100, 200]: # Vector size of embeddings
        print(algo, vsize)

        embeddingPath = os.path.join(dataLocation, "embeddings", f"embeddings_{algo}_{vsize}")
        
        evaluation_manager = FrameworkManager()
        evaluation_manager.evaluate(
            embeddingPath,
            tasks=["Classification"],
            parallel=False,
            debugging_mode=False,
            vector_size=vsize,
            result_directory_path=os.path.join(evalPath, f"geval_result_{algo}_{vsize}")
        )
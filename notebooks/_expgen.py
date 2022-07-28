import os
import pandas as pd
import pickle
from importlib import reload
import lime.lime_rdf
import logging
from rdflimeConfig import datasets, load_dataset, split_dataset
from pathlib import Path

logging.basicConfig(level=logging.WARN)

algo = "cbow"
vsize = 100
svc_c = 10
explored_dataset_idx = 2
n = 40

dataset_full, dataset_entities = load_dataset(datasets[explored_dataset_idx], fixed=True)
cfg = datasets[explored_dataset_idx]
uri_col = cfg["columns"]["uri_fixed"]
label_col = cfg["columns"]["label"]

# Will yield the same train/test split that has been used for training the final classifier
dataset_train, dataset_test = split_dataset(dataset_full, cfg, randomize=True)

def gen_exp(explained_idx):
    # Load classifier
    with open(os.path.join(cfg["location"], "classifiers", f"svc_{svc_c}_{algo}_{vsize}"), "rb") as file:
        clf = pickle.load(file)

    # Load RDF2Vec Transformer
    with open(os.path.join(cfg["location"], "transformers", f"rdf2vec_transformer_{algo}_{vsize}"), "rb") as file:
        rdf2vec_transformer = pickle.load(file)

    entity_kind = cfg["entity"]
    print(f"Ready to explain {algo}_{vsize} classifier predictions for {entity_kind}.")

    reload(lime.lime_rdf)
    from lime.lime_rdf import LimeRdfExplainer

    # TODO ! Check if entities in correct order

    explainer = LimeRdfExplainer(
        transformer=rdf2vec_transformer, 
        entities=dataset_entities,
        class_names=clf.classes_,
        kernel=None,
        kernel_width=25,
        verbose=False,
        feature_selection="auto",
        random_state=42
    )

    # Attention: Index value, not row number!
    explained_entity_row = dataset_full.loc[explained_idx]
    explained_entity_uri = explained_entity_row[uri_col]
    embedding = rdf2vec_transformer._embeddings[rdf2vec_transformer._entities.index(explained_entity_uri)]
    prediction = clf.predict_proba([embedding])

    print("Explaining", explained_entity_uri)
    print("Original prediction:", prediction, " / ".join(clf.classes_))
    print("True class:", explained_entity_row[label_col])

    data, probabilities, distances, explanation = explainer.explain_instance(
        entity=explained_entity_uri, 
        classifier_fn=clf.predict_proba,
        num_features=50,
        num_samples=5000,
        allow_triple_addition=False,
        allow_triple_subtraction=True,
        max_changed_triples=20,
        change_count_fixed=True,
        use_w2v_freeze=True,
        center_correction=False,
        single_run=False,
        train_with_all=False,
        distance_metric="cosine",
        model_regressor=None,
        short_uris=False,
        labels=(0,1,2)
    )

    targetPath = os.path.join(cfg["location"], "explanations")
    Path(targetPath).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(cfg["location"], "explanations", f"svc_{svc_c}_{algo}_{vsize}_{explained_idx}"), "wb") as f:
        pickle.dump((data,probabilities,distances,explanation,prediction,explainer.indexed_walks,explained_entity_uri,explained_idx), f)

candidates = dataset_test.sample(frac=1, random_state=21) #.sample(n=n, random_state=42)
for idx, candidate in candidates.iterrows():
    if os.path.exists(os.path.join(cfg["location"], "explanations", f"svc_{svc_c}_{algo}_{vsize}_{idx}")):
        print("Skipping", idx)
        continue
    print(idx, candidate)

    if explored_dataset_idx == 2 and idx == 87:
        print("Skipping - ", idx)
        continue # Wrong entity with very few walks; now corrected in original dataset.

    gen_exp(idx)
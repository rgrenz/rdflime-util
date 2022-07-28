import os
from pathlib import Path
import pandas as pd
import pickle
from importlib import reload
import lime.lime_rdf
import logging
from rdflimeConfig import datasets, load_dataset, split_dataset
import matplotlib.pyplot as plt
import numpy as np
from textwrap import wrap

logging.basicConfig(level=logging.WARN)

COLOR_POSITIVE = "#009E73"
COLOR_NEGATIVE = "#D55E00"
COLOR_NEUTRAL = "#000000"

explored_dataset_idx = 2
cfg = datasets[explored_dataset_idx]

exp_path = os.path.join(cfg["location"], "explanations")
files = [f for f in os.listdir(exp_path) if os.path.isfile(os.path.join(exp_path, f))]

for file in files:

    if not file.endswith("_776"):
        continue

    with open(os.path.join(exp_path, file), "rb") as f:
        data, probabilities, distances, explanation, prediction, indexed_walks, entity_uri, entity_idx = pickle.load(f)

    prediction = prediction[0]
    predicted_idx = np.argmax(prediction)
    predicted_label = explanation.class_names[predicted_idx]
    predicted_label_probability = prediction[predicted_idx]
    print(f"{entity_idx} {entity_uri}", f"classified as {predicted_label} ({predicted_label_probability})", prediction)

    print(explanation.score)
    

    for label_idx in range(len(prediction)):

        if explored_dataset_idx < 2 and label_idx == 0:
            continue # Explanations have only been generated for one label in the binary datasets

        ##### Bar chart
        bar_path = os.path.join(exp_path, "bar-chart")
        Path(bar_path).mkdir(parents=True, exist_ok=True)
        figsize = (5, .18*len(explanation.as_list(label=label_idx)))
        explanation.domain_mapper.short_uris=True
        # fig = explanation.as_pyplot_figure(figsize=figsize)
        # Contents of as_pyplot_figure (to allow for modifications for the printed thesis)
        exp = explanation.as_list(label=label_idx)[:25]
        fig = plt.figure(figsize=figsize)
        vals = [x[1] for x in exp]
        names = [x[0] for x in exp] # "\n".join(wrap(str(x[0]),75))
        vals.reverse()
        names.reverse()
        colors = [COLOR_POSITIVE if x > 0 else COLOR_NEGATIVE for x in vals]
        pos = np.arange(len(exp)) + .5
        plt.barh(pos, vals, align='center', color=colors)
        plt.yticks(pos, names)
        title = f'Local explanation for class {explanation.class_names[label_idx]} (p={prediction[label_idx]:.2f})' 
        plt.title(title)
        explanation.domain_mapper.short_uris=False
        plt.savefig(os.path.join(bar_path, file+f"_{label_idx}.pdf"), format="pdf", bbox_inches="tight")

        """
        import mpld3
        mpld3.plugins.clear(fig)
        mpld3.plugins.connect(fig, mpld3.plugins.Reset(), mpld3.plugins.Zoom(button=True, enabled=True))
        Path(os.path.join(bar_path, "interactive")).mkdir(parents=True, exist_ok=True)
        mpld3.save_html(fig, os.path.join(bar_path, "interactive", file+f"_{label_idx}.html"))
        """

        plt.close()


        ##### Graph vis
        graph_path = os.path.join(exp_path, "graph-visualization")
        graph_pdf_path = os.path.join(graph_path, "pdf")
        Path(graph_pdf_path).mkdir(parents=True, exist_ok=True)

        #### Get list of relevant triples (top_triples and their connectors)
        iw = indexed_walks

        top_triples = explanation.as_list(label=label_idx)[:15]

        relevant_walks = []
        for triple in top_triples:
            for w in iw.walks(entity_uri, tuple(triple[0])):
                
                entity_pos = w.index(entity_uri)

                for i in range(2, len(w)):
                    if w[i-2]== triple[0][0] and w[i-1] == triple[0][1] and w[i] == triple[0][2]:
                        triple_start_pos = i-2
                        triple_end_pos = i
                
                from_pos = min(entity_pos, triple_start_pos)
                to_pos = max(entity_pos, triple_end_pos)

                relevant_walks.append(w[from_pos:to_pos+1])
        

        relevant_triples = iw.walks_as_triples(relevant_walks)

        #### Build graph structure
        edges = []
        labels = {}

        min_edge_width = 0.25
        max_edge_width = 8
        max_score = max([abs(exp[1]) for exp in top_triples])

        uri_trimmer = lambda uri: uri.split("/")[-1].split("#")[-1].replace(":", "_")
        triple_trimmer = lambda triple: (uri_trimmer(triple[0]), uri_trimmer(triple[1]), uri_trimmer(triple[2]))

        for rt in relevant_triples:
            score = next((exp[1] for exp in top_triples if rt==exp[0]), None)
            
            if score:
                # score *= -1
                color =  COLOR_POSITIVE if score > 0 else COLOR_NEGATIVE
                width = max(abs(score)/max_score*max_edge_width, min_edge_width)
            else:
                color = COLOR_NEUTRAL
                width = min_edge_width
                #print(rt, score)

            rt = triple_trimmer(rt)
            edge = (rt[0] or "(blank)", rt[2] or "(blank)", {"width": width, "color": color})

            if edge[0] == edge[1]:
                continue # Due to bug in mpld3 HTTP export
            if not edge[0] or not edge[1]:
                continue # Empty
            
            # Multigraph relations are plotted confusingly - graphviz lib does not not handle multigraphs well
            skip_insertion = False
            for e in edges:
                if (e[0], e[1]) == (edge[0], edge[1]) or (e[0], e[1]) == (edge[1], edge[0]):
                    if e[2]["width"] >= edge[2]["width"]:
                        skip_insertion = True
                    else:                 
                        edges.remove(e)
            
            label = rt[1]
            if score: label += f" ({round(width/max_edge_width, 2)})"

            if not skip_insertion:
                edges.append(edge)
                labels[(edge[0],edge[1])] = label

        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        import networkx as nx
        from math import sqrt
        import mpld3

        f = plt.figure(figsize=(25,26)) # 19, 15
        plt.title(f"Local explanation for class {explanation.class_names[label_idx]} (p={prediction[label_idx]:.2f})")
        positive_patch = mpatches.Patch(color=COLOR_POSITIVE, label='Positive influence')
        negative_patch = mpatches.Patch(color=COLOR_NEGATIVE, label='Negative influence')
        plt.legend(handles=[positive_patch, negative_patch])
        plt.axis("off")

        G = nx.MultiDiGraph()
        G.add_edges_from(edges)
        # pos = nx.spring_layout(G, k=1.25/sqrt(len(G.nodes())), seed=42, iterations=35)
        pos = nx.nx_agraph.graphviz_layout(G, prog="neato")

        nx.draw(
            G, pos,
            node_size=500, node_color='lightblue', alpha=0.9,
            labels={node: node for node in G.nodes()},
            arrowstyle='->',
            width=[G[u][v][0]['width'] for u,v in G.edges()],
            edge_color=[G[u][v][0]['color'] for u,v in G.edges()],
            style=["dotted" if G[u][v][0]['color'] == COLOR_NEGATIVE else "-" for u,v in G.edges()], # :
        )


        _ = nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels=labels,
            font_color='black',
            verticalalignment="center",
            bbox={"boxstyle":'round', "ec":(1.0, 1.0, 1.0), "fc":(1.0, 1.0, 1.0)}
        )

        f.tight_layout()
        # plt.savefig("test.svg")
        mpld3.plugins.clear(f)
        mpld3.plugins.connect(f, mpld3.plugins.Reset(), mpld3.plugins.Zoom(button=True, enabled=True))
        mpld3.save_html(f, os.path.join(graph_path, file+f"_{label_idx}_t.html"))
        plt.savefig(os.path.join(graph_pdf_path, file+f"_{label_idx}_t.pdf"))
        plt.close()
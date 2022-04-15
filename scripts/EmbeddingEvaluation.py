from evaluation_framework.manager import FrameworkManager
import os 

if __name__ == "__main__":

    for algo in ["cbow","sg"]:
        for vsize in [50,100,200]: # Vector size of embeddings
            print(algo, vsize)
            p = os.path.join("/home/rouven/work/unima/rdflime/lime/rdflime/data/metacritic-movies", f"embeddings_{algo}_{vsize}")
   
            evaluation_manager = FrameworkManager()
            evaluation_manager.evaluate(
                p,
                tasks=["Classification"],
                parallel=False,
                debugging_mode=True,
                vector_size=vsize
            )

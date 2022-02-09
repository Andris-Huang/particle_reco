import itertools
import importlib
import numpy as np


base_file = importlib.import_module(f"src.models.base")
blankBase = base_file.Base

class Base(blankBase):
    """
    The base file for a clustering task.
    """
    
    def predict(self, solver, graph):
        """
        Predict clusters given solver and event
        """
        uncut_edges = solver(graph, self.output_dir, self.save_fig, 
                             config=self.config, return_edge=True)
        pred = []
        edge_dict = graph["edge_labels"]
        for e in edge_dict:
            if e in uncut_edges:
                pred.append(1)
            else:
                pred.append(0)

        return pred
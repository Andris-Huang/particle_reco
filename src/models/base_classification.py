import itertools
import importlib
import numpy as np


base_file = importlib.import_module(f"src.models.base")
blankBase = base_file.Base

class Base(blankBase):
    """
    The base file for a classification task.
    """
    
    def predict(self, solver, graph):
        """
        Predict taus given solver and event
        """
        S0, S1 = solver(graph, self.output_dir, self.save_fig, config=self.config)
        if len(S1) == 2:
            S0, S1 = S1, S0
        elif len(S0) != 2:
            print("The maxcut solver has identified wrong number of jets.")
        pred = list(graph["nodes"])
        for n in S0:
            pred[n] = 1
        for n in S1:
            pred[n] = 0
        for i in range(len(pred)):
            if pred[i] != 0 and pred[i] != 1:
                print("Some jets do not have a prediction.")
                pred[i] = 0
        return np.array(pred, dtype=np.int8)
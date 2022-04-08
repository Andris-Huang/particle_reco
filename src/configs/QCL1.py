from qiskit.aqua.components.optimizers import SPSA, COBYLA
from qiskit.circuit.library import ZZFeatureMap, TwoLocal, EfficientSU2

NQUBIT = 3
feature_dim = NQUBIT   # dimension of each data point
if feature_dim == 3:
    SelectedFeatures = ['lep1_pt', 'lep2_pt', 'miss_ene']
elif feature_dim == 5:
    SelectedFeatures = ['lep1_pt','lep2_pt','miss_ene','M_TR_2','M_Delta_R']
elif feature_dim == 7:
    SelectedFeatures = ['lep1_pt','lep1_eta','lep2_pt','lep2_eta','miss_ene','M_TR_2','M_Delta_R']

config = {
    "model": "QCL",
    "input_dir": None,
    "output_dir": None,
    "num_evt": 100,
    "num_job": 10,
    "encoder_depth": 3,
    "vqc_depth": 4,
    "num_iter": 4,
    "shots": 1024,
    "optimizer": COBYLA,
    "feature_map": ZZFeatureMap,
    "var_form": EfficientSU2,
    "features": SelectedFeatures,
    "backend": "aer_simulator"
}
from qiskit.aqua.components.optimizers import SPSA, COBYLA
from qiskit.circuit.library import ZZFeatureMap, TwoLocal, EfficientSU2


config = {
    "model": "QCL",
    "input_dir": "../datasets/gamma_ditau.csv",
    "output_dir": "outputs/gamma_ditau",
    "num_evt": 100,
    "num_job": 10,
    "encoder_depth": 3,
    "vqc_depth": 4,
    "num_iter": 4,
    "shots": 1024,
    "optimizer": COBYLA,
    "feature_map": ZZFeatureMap,
    "var_form": EfficientSU2,
    "features": ['JetPt', 'JetEta', 'JetPhi'],
    "backend": "aer_simulator"
}
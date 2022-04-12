import optuna
import os
import warnings
import itertools
import importlib
import sys
import argparse
warnings.filterwarnings('ignore')

from qiskit.aqua.components.optimizers import SPSA, COBYLA
from qiskit.circuit.library import ZZFeatureMap, TwoLocal, EfficientSU2

def create_study(start_new=True, count=0):
    """
    Create a study for parameter tuning.
    """
    study_folder = 'HPO'
    CWD = os.getcwd()
    folder_path = os.path.join(CWD, study_folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    SEED = 9855502
    #count = 0
    while True:
        study_name = f"HPO_{count}"
        study_path = os.path.join(study_folder, study_name)
        storage_name  = "sqlite:///{}.db".format(study_path)
        if start_new:
            try:
                study = optuna.create_study(direction='maximize',study_name=study_path, 
                                            storage=storage_name,load_if_exists=False, 
                                            sampler=optuna.samplers.TPESampler(seed=SEED))
            except optuna.exceptions.DuplicatedStudyError:
                count += 1
            else:
                break
        else:
            study = optuna.create_study(direction='maximize',study_name=study_path, 
                                            storage=storage_name,load_if_exists=True, 
                                            sampler=optuna.samplers.TPESampler(seed=SEED))
            break
    return study


def objective(trial):
    """
    Defines an objective that we try to optimze. In this project, it's the AUC for classification. 
    Simply run this block.
    
    Args:
        trial (object): a specific trial with given combinations of parameters
        
    Returns:
        -1 if the given combination of param is not compatible with the model;
    """
    num_job = trial.suggest_int('num_job', 10, 50)
    encoder_depth = trial.suggest_int('encoder_depth', 1, 5)
    vqc_depth = trial.suggest_int('vqc_depth', 1, 5)
    num_iter = trial.suggest_int('num_iter', 1, 5)
    optimizer = trial.suggest_categorical('optimizer', ['COBYLA'])
    feature_map = trial.suggest_categorical('feature_map', ['ZZFeatureMap'])
    var_form = trial.suggest_categorical('var_form', ['EfficientSU2'])
    
    high_level_var = ['JetCentralEFrac', 'JetLeadingTrackFracP', 'JetTrackR', 'JetMaxDRInCore',
                      'JetNumISOTracks', 'JetLeadingTrackD0','JetTrackMass']
    four_vec = ['JetPt', 'JetEta', 'JetPhi', 'JetE']
    mixed_var = [list(i) for i in itertools.combinations(high_level_var, 3)]
    all_feature_options = [four_vec] + mixed_var + [high_level_var]
    features = trial.suggest_categorical('features', all_feature_options)
    
    config = {
        "model": "QCL",
        "input_dir": "../datasets/gamma_ditau.csv",
        "output_dir": "outputs/gamma_ditau",
        "num_evt": 40,
        "num_job": num_job,
        "encoder_depth": encoder_depth,
        "vqc_depth": vqc_depth,
        "num_iter": num_iter,
        "shots": 1024,
        "optimizer": eval(optimizer),
        "feature_map": eval(feature_map),
        "var_form": eval(var_form),
        "features": features,
        "backend": "aer_simulator"
    }
    
    try:
        model_name = config['model']
        model_file = importlib.import_module(f"src.models.{model_name}")
        model_class = model_file.Model

        model = model_class(config, save_fig=False, overwrite=False, debug=False, hide_display=True)
        model.train()
        return model.evaluate()[1] # Testing AUC
    except:
        return -1 # the given combination of param is not compatible with the model
    
    
parser = argparse.ArgumentParser(description='HPO')
add_arg = parser.add_argument
add_arg("-c", "--continue", dest="start_new", help="If continue on previous tuning", action='store_false', default=True)
add_arg("-i","--count", dest="start_count", help="The index of preivous tuning study", type=int, default=0) 
add_arg("-t", dest='timeout', help="Time out in seconds", type=int, default=60)

args = parser.parse_args()
study = create_study(args.start_new, args.start_count)
study.optimize(objective, n_trials=50, timeout=30*60) # Can change the number of trials and timeout (in seconds)

# Print the best stats
print("Best trial:")
trial = study.best_trial
print("  Value: ", trial.value)
print("  Params: ")
for key, value in trial.params.items():
    print("    {}: {}".format(key, value))
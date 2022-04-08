import pandas as pd

class QMLBase:
    """
    The base file for QML tasks.
    """
    def __init__(self, config, save_fig=True, overwrite=False, debug=False):
        self.base_params = {}
        self.save_fig = save_fig
        self.overwrite = overwrite
        self.debug = debug
        self.input_dir = config['input_dir']
        self.output_dir = config['output_dir']
        
    
    def _process_config(self, config):
        new_config = config
        for param in self.base_params:
            if param not in self.config:
                new_config[param] = self.base_params[param]
        return new_config

    def process_data(self):
        
        df = pd.read_csv(self.input_dir)
        if "num_evt" not in self.config or self.config["num_evt"] is None:
            self.nevt = self.config["num_evt"] = len(df)
        else:
            self.nevt = self.config["num_evt"]
        if "training_size" not in self.config:
            self.config["training_size"] = 0.7 * self.nevt
        if "testing_size" not in self.config:
            self.config["testing_size"] = 0.3 * self.nevt

        SelectedFeatures = self.config["features"]
        training_size = self.config["training_size"]
        testing_size = self.config["testing_size"]

        df_sig = df.loc[df.isSignal==1, SelectedFeatures]
        df_bkg = df.loc[df.isSignal==0, SelectedFeatures]

        df_sig_training = df_sig.values[:training_size]
        df_bkg_training = df_bkg.values[:training_size]
        df_sig_test = df_sig.values[training_size:training_size+testing_size]
        df_bkg_test = df_bkg.values[training_size:training_size+testing_size]
        training_input = {'1':df_sig_training, '0':df_bkg_training}
        test_input = {'1':df_sig_test, '0':df_bkg_test}

        return training_input, test_input

    def model(self):
        raise NotImplementedError

    def train(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError

    def evaluate(self):
        raise NotImplementedError

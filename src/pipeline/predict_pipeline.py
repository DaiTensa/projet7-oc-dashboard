import pandas as pd
from src.utilis import load_object
from src.components.data_config import AppConfig
import numpy as np


class DataClient:
    def __init__(self):
        self.data_preprocessor_model_path = AppConfig()
        self.df_clients= pd.read_csv(self.data_preprocessor_model_path.clients_data__path)
        self.preprocessor= load_object(url_path=self.data_preprocessor_model_path.preprocessor_ob_file__path)
        self.model= load_object(url_path=self.data_preprocessor_model_path.trained_model_file__path)
        self.explainer = load_object(url_path=self.data_preprocessor_model_path.explainer__path)

    
    def gest_local_explanation(self, df):
        df = df.replace((np.inf, -np.inf), np.nan).reset_index(drop=True)
        data_scaled= self.preprocessor.transform(df)
        data_scaled = pd.DataFrame(data_scaled, columns= list(df.columns))
        shap_values = self.explainer.shap_values(data_scaled.loc[0])
        test_ = pd.DataFrame(shap_values, index= list(data_scaled.columns), columns=['shape_values'])
        test_ = test_.reset_index()
        test_ = test_.rename(columns={'index': 'Features'})
        return test_
    
    def liste_id_clients(self):
        return self.df_clients.SK_ID_CURR.unique()

    def liste_columns(self):
        return self.df_clients.columns

    def get_data_as_df(self, ID_client):
        ID_client = int(ID_client)
        df_client= (self.df_clients.loc[self.df_clients["SK_ID_CURR"] == ID_client]).copy()
        df_client = df_client.drop(["SK_ID_CURR"], axis=1)
        return df_client

    def predict_function(self, df):
        df = df.replace((np.inf, -np.inf), np.nan).reset_index(drop=True)
        data_scaled= self.preprocessor.transform(df)
        data_scaled = pd.DataFrame(data_scaled, columns= list(df.columns))
        # pred= self.model.predict(data_scaled)
        pred= self.model.predict_proba(data_scaled)
        # predicted_classe = pred[0]
        return {"solvable": bool(pred[0][0] > 0.5), "seuil": 0.5, "proba" : pred[0][0]}

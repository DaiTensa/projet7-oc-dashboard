import pytest
import pandas as pd

clients_data__path = "https://raw.githubusercontent.com/DaiTensa/dashboard/main/reduced_test.csv"

data_clients = pd.read_csv(clients_data__path)

def get_data_as_df(df_clients, ID_client):
    ID_client = int(ID_client)
    df_client= (df_clients.loc[df_clients["SK_ID_CURR"] == ID_client]).copy()
    return df_client


ID_CLIENT = 100038

df_client = get_data_as_df(data_clients, ID_client= ID_CLIENT)

@pytest.mark.infos_clients
def test_infos_du_client(df_client):
    assert df_client.loc[df_client["SK_ID_CURR"] == 100038 , 'CODE_GENDER'] == 1
    assert df_client.loc[df_client["SK_ID_CURR"] == 100038 , 'AMT_INCOME_TOTAL'] == 180000
    assert df_client.loc[df_client["SK_ID_CURR"] == 100038 , 'AMT_CREDIT'] == 625500

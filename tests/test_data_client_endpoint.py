import pytest
import pandas as pd


@pytest.mark.infos_clients
def test_infos_du_client():
    clients_data__path = "https://raw.githubusercontent.com/DaiTensa/dashboard/main/reduced_test.csv"
    data_clients = pd.read_csv(clients_data__path)
    df_client= (data_clients.loc[data_clients["SK_ID_CURR"] == 100038]).copy()
    assert df_client.loc[df_client["SK_ID_CURR"] == 100038 , 'CODE_GENDER'] == 1
    assert df_client.loc[df_client["SK_ID_CURR"] == 100038 , 'AMT_INCOME_TOTAL'] == 180000
    assert df_client.loc[df_client["SK_ID_CURR"] == 100038 , 'AMT_CREDIT'] == 625500

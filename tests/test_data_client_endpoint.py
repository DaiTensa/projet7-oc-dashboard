import pytest
from predict_pipeline import DataClient


data_clients = DataClient()
ID_CLIENT = 100038

df_client = data_clients.get_data_as_df(ID_client= int(ID_CLIENT))

@pytest.mark.infos_clients
def test_infos_du_client():
    assert df_client['CODE_GENDER'] == 1
    assert df_client['AMT_INCOME_TOTAL'] == 180000
    assert df_client['AMT_CREDIT'] == 625500

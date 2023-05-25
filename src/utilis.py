import dill
import requests
import io


def load_object(url_path):
    response = requests.get(url_path)
    content = response.content
    return dill.load(io.BytesIO(content))
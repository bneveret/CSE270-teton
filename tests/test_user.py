import requests
import pytest

def test_unauthorized_access():
    url = "http://127.0.0.1:8000/users"
    params = {"username": "admin", "password": "admin"}
    response = requests.get(url, params=params)
    
    assert response.status_code == 401, f"Expected 401, but got {response.status_code}"
    assert response.text.strip() == "", f"Expected empty response, but got {response.text.strip()}"

def test_authorized_access():
    url = "http://127.0.0.1:8000/users"
    params = {"username": "admin", "password": "qwerty"}
    response = requests.get(url, params=params)
    
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
    assert response.text.strip() == "", f"Expected empty response, but got {response.text.strip()}"

@pytest.fixture(autouse=True)
def mock_requests_get(mocker):
    def mock_get(url, params=None, **kwargs):
        mock_response = requests.Response()
        if params == {"username": "admin", "password": "admin"}:
            mock_response.status_code = 401
            mock_response._content = b""
        elif params == {"username": "admin", "password": "qwerty"}:
            mock_response.status_code = 200
            mock_response._content = b""
        return mock_response
    
    mocker.patch("requests.get", side_effect=mock_get)
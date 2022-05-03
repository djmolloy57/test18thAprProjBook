import pytest
import requests
import json 

#test api site https://reqres.in/ 


def test_valid_login():
    url = "https://reqres.in/api/login"
    data = {'email' : 'abx@test.com', 'password' : 'querty'}
    response = requests.post(url, data=data)
    t = json.loads(response.text)
    assert response.status_code == 200
    assert t['token'] == "QpwL5tke4Pnpja7X"



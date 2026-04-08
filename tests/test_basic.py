from app.main import app

def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "UP"

def test_add():
    client = app.test_client()
    res = client.get("/add/2/3")
    assert res.status_code == 200
    assert res.get_json()["result"] == 5

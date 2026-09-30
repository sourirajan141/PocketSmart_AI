from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_startup():
    r=client.get('/startup'); assert r.status_code==200

def test_register_login():
    email='test@example.com'
    client.post('/api/register',json={'name':'Test User','email':email,'password':'secret123'})
    r=client.post('/api/login',json={'email':email,'password':'secret123'}); assert r.status_code==200; assert 'access_token' in r.json()

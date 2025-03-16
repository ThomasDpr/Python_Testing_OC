import pytest

from server import app


@pytest.fixture
def client():
    """
    Fixture qui crée un client de test pour l'application Flask.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_empty_email(client):
    """Test avec un email vide"""
    response = client.post('/showSummary', data={'email': ''}, follow_redirects=True)
    assert b"Email field is required" in response.data

def test_invalid_email_format(client):
    """Test avec un email au format invalide"""
    response = client.post('/showSummary', data={'email': 'invalid.email'}, follow_redirects=True)
    assert b"Invalid email format" in response.data

def test_unknown_email(client):
    """Test avec un email qui n'existe pas dans la base"""
    response = client.post('/showSummary', data={'email': 'unknown@email.com'}, follow_redirects=True)
    assert "email wasn" in response.data.decode()  # On vérifie juste une partie du message

def test_valid_email(client):
    """Test avec un email valide"""
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
    assert b"Welcome" in response.data
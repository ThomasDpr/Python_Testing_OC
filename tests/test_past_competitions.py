from datetime import datetime, timedelta

import pytest

from server import app, is_past_competition


@pytest.fixture
def client():
    """Fixture qui crée un client de test pour l'application Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_past_competition_checker():
    """Test de la fonction is_past_competition"""
    # Date passée
    past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    assert is_past_competition(past_date) is True

    # Date future
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    assert is_past_competition(future_date) is False

def test_booking_past_competition(client):
    """Test de la tentative de réservation d'une compétition passée"""
    # D'abord se connecter
    client.post('/showSummary', data={'email': 'john@simplylift.co'})
    
    # Essayer de réserver une compétition passée (Spring Festival)
    response = client.get('/book/Spring Festival/Simply Lift')
    assert "Cannot book Spring Festival because it is a past competition" in response.data.decode()

def test_booking_page_access(client):
    """Test l'accès à la page de réservation pour les différentes compétitions"""
    # D'abord se connecter
    client.post('/showSummary', data={'email': 'john@simplylift.co'})
    
    # Tester Spring Festival (passée)
    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200
    assert "Cannot book Spring Festival because it is a past competition" in response.data.decode()
    
    # Tester Fall Classic (passée)
    response = client.get('/book/Fall Classic/Simply Lift')
    assert response.status_code == 200
    assert "Cannot book Fall Classic because it is a past competition" in response.data.decode()
import pytest

from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_booking_more_than_12_places(client):
    """Test qu'un club ne peut pas réserver plus de 12 places"""
    # Connexion
    client.post('/showSummary', data={'email': 'john@simplylift.co'})
    
    # Tenter de réserver plus de 12 places
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '13'  # Essaie de réserver 13 places
    })
    
    assert "You can only book up to 12 places per competition" in response.data.decode()


def test_booking_exactly_12_places(client):
    """Test qu'un club peut réserver exactement 12 places"""
    # Connexion
    client.post('/showSummary', data={'email': 'john@simplylift.co'})
    
    # Réserver 12 places
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'test',
        'places': '12'
    })
    
    assert "Great-booking complete!" in response.data.decode()
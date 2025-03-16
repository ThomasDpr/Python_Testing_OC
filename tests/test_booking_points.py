import pytest

from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_booking_more_points_than_available(client):
    """Test qu'un club ne peut pas réserver plus de places qu'il n'a de points"""
    # Connexion
    client.post('/showSummary', data={'email': 'john@simplylift.co'})

    # Tenter de réserver plus de places que de points disponibles
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',  # Club avec 13 points
        'competition': 'test',
        'places': '14'  # Nombre > 13 pour tester l'erreur
    })

    assert "Not enough points available!" in response.data.decode()
def test_points_deducted_correctly(client):
    """Test que les points sont correctement déduits après une réservation valide"""
    # Connexion
    client.post('/showSummary', data={'email': 'john@simplylift.co'})
    
    # Réserver un nombre valide de places
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '5'
    })
    
    assert "Great-booking complete!" in response.data.decode()
    # Vérifier que les points ont été correctement déduits (13 - 5 = 8)
    assert '8' in response.data.decode()
    
def test_booking_negative_places(client):
    """Test qu'on ne peut pas réserver un nombre négatif de places"""
    # Connexion
    client.post('/showSummary', data={'email': 'john@simplylift.co'})
    
    # Tenter de réserver un nombre négatif de places
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'test',
        'places': '-5'
    })
    
    assert "You cannot book a negative or null number of places" in response.data.decode()

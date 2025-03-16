"""
Module de test pour la fonctionnalité d'affichage du tableau des points.
Ce module contient des tests qui vérifient :
- L'accessibilité publique du tableau des points
- L'affichage correct des données des clubs
- La cohérence des données avec le fichier clubs.json
"""

import json

import pytest

from server import app

# Note à moi même pour mes tests : 
# assert est une instruction utilisée pour vérifier qu'une condition est vraie. 
# Si la condition est fausse : assert lève une exception et le test échoue. 


@pytest.fixture                         # <----- Décorateur qui indique à pytest que c'est une fixture réutilisable
def client():
    """
    Fixture qui crée un client de test pour l'application Flask.
    
    Retourne:
        FlaskClient: Un client de test qui peut être utilisé pour simuler des requêtes HTTP.
    """
    app.config['TESTING'] = True        # <----- Active le mode test de Flask pour désactiver certaines protections et optimiser pour les tests
    with app.test_client() as client:   # <----- Crée un client de test Flask qui peut simuler des requêtes HTTP comme un vrai navigateur
        yield client                    # <----- Fournit le client aux tests et s'assure qu'il sera bien fermé après utilisation

def test_points_board_access(client):
    """
    Test de l'accessibilité de la page du tableau des points.
    
    Ce test vérifie que :
    - La route /points est accessible publiquement
    - La page renvoie un code de statut HTTP 200
    - Aucune authentification n'est requise pour accéder à la page
    
    Arguments:
        client (FlaskClient): La fixture du client de test
    """
    response = client.get('/points')    # <----- Envoie une requête GET à la route '/points' en utilisant le client de test
    assert response.status_code == 200  # <----- Vérifie que le code de statut HTTP de la réponse est 200 (OK)
    
def test_points_board_content(client):
    """
    Test du contenu affiché dans le tableau des points.
    
    Ce test vérifie que :
    - Tous les clubs du fichier clubs.json sont affichés
    - Le nom de chaque club est correctement affiché
    - La valeur des points de chaque club est affichée avec précision
    - Les données correspondent au fichier JSON source
    
    Arguments:
        client (FlaskClient): La fixture du client de test
    """ 
    # Charger les données du fichier clubs.json
    with open('clubs.json') as f:
        clubs_data = json.load(f)['clubs']
    
    response = client.get('/points')
    
    # Vérifier que chaque club est présent dans la réponse
    for club in clubs_data:
        assert club['name'] in response.data.decode()
        assert club['points'] in response.data.decode()
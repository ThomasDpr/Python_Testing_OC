import json

import pytest

import server


@pytest.fixture(autouse=True)
def setup_test_data():
    """Réinitialise les données avant chaque test"""
    # Recharger les données originales

    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()
    
    
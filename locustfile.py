from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Simulation d'un délai entre les requêtes

    @task
    def load_homepage(self):
        """Test du temps de chargement de la page d'accueil"""
        self.client.get("/")

    @task
    def login_and_view_competitions(self):
        """Test du temps de chargement après connexion"""
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def book_places(self):
        """Test de la vitesse de réservation"""
        self.client.post("/purchasePlaces", data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "3"
        })

    @task
    def view_points_board(self):
        """Test du chargement de la page des points"""
        self.client.get("/points")

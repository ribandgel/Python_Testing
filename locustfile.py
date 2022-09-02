from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task(5)
    def summary(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task(1)
    def book(self):
        self.client.get("/book/Spring Festival/Simply Lift")

    @task(1)
    def purchase(self):
        self.client.post("/purchasePlaces", {"competition": "Spring Festival", "club": "Simply Lift", "places": 1})

    @task(1)
    def index(self):
        self.client.get("/")
from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Random wait time between 1 and 3 seconds

    @task
    def recommend(self):
        headers = {'Content-Type': 'application/json'}
        data = {
            "product_name": "T-Shirt"
        }
        self.client.post("/recommend", json=data, headers=headers)


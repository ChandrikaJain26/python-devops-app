from locust import HttpUser, task, between

class DevOpsUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def health_check(self):
        self.client.get("/health")

    @task
    def add_test(self):
        self.client.get("/add/2/3")


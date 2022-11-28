from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def apex_main(self):
        self.client.get("/265")

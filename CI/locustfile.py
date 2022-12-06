import csv

# import logging
import os
import time

from locust import SequentialTaskSet, between, task
from locust_plugins.users import RestUser
from rest_framework import status

cur_path = os.getcwd()
file_path = os.path.join(cur_path, "dummies.csv")
host_url = "https://apexacademy.com.np"
# host_url = "http://localhost:8000"

USER_CREDENTIALS = []

with open(file_path, "r") as f:
    reader = csv.reader(f)
    USER_CREDENTIALS = list(reader)


class HelloWorldUser(RestUser):
    # @task
    # def apex_main(self):
    #     self.client.get("/")
    #     self.client.get("https://apexacademy.com.np")
    # host = "https://apexacademy.com.np"
    wait_time = between(1, 5)  # pause between each task
    host = host_url
    # host = "https://apexacademy.com.np"

    @task
    class LoginExamFlow(SequentialTaskSet):
        def on_start(self):
            print(USER_CREDENTIALS)
            if len(USER_CREDENTIALS) <= 0:
                # exit the test
                self.interrupt()
            self.username, self.password = USER_CREDENTIALS.pop()
            print(self.username, self.password)

        # def on_start(self):
        #     self.client.post("/login", {"username": "test", "password": "test"})
        access_token = ""
        refresh_token = ""
        enroll_id = ""
        sel_sess = 552

        @task
        def login(self):
            with self.client.request(
                "POST",
                f"{host_url}/api/auth/login/",
                json={
                    "username": f"{self.username}",
                    "email": "",
                    "password": f"{self.password}",
                },
                catch_response=True,
            ) as resp:
                if resp.status_code == 200:
                    print("Login Successful")
                    self.access_token = resp.json()["access_token"]
                    self.refresh_token = resp.json()["refresh_token"]
                    # save the login
                else:
                    print(resp.json())
                    print("Failed to login")

        # save the login token and do an exam

        @task
        def exam_enroll(self):
            with self.client.request(
                "POST",
                f"{host_url}/api/enrollments/create/",
                catch_response=True,
                json={"exams": [{"exam": "256", "selected_session": self.sel_sess}]},
            ) as resp:
                if resp.status_code in [200, status.HTTP_201_CREATED]:
                    print("Exam Successful")
                    self.enroll_id = resp.json()["exams"][0]["id"]
                    print(resp.json())

                else:
                    print("Failed to get enroll into exam")
                    print(resp.status_code)
                    print(resp.json())

        @task
        def get_questions(self):
            url = f"{host_url}/api/exams/paper/256/{self.sel_sess}/"
            print(url)
            with self.client.request(
                "GET",
                url,
                catch_response=True,
            ) as resp:
                if resp.status_code == 200:
                    print("Questioned obtained sucessfully")
                    # print(resp.json())
                    # save the login
                else:
                    print("Failed to get questions")
                    print(resp)

        @task
        def exam_retrieve(self):
            with self.client.request(
                "GET",
                f"{host_url}/api/exams/retrieve/256/",
                catch_response=True,
            ) as resp:
                if resp.status_code == 200:
                    print("Exam retrieved Successfully")
                    # save the login
                    # print(resp.json())
                else:
                    print("Failed to retrieve exam")
                    print(resp)

        @task
        def attempt_exam_pg1(self):
            url = f"{host_url}/api/enrollments/exam/submit/{self.enroll_id}"
            print(url)
            with self.client.request(
                "PUT",
                url,
                catch_response=True,
                json={
                    "question_states": [
                        {"question": 16173, "selected_option": 64691},
                        {"question": 16174, "selected_option": 64693},
                    ],
                    "submitted": False,
                },
            ) as resp:
                if resp.status_code == 200:
                    print("first page attempt Successful")
                    # save the login
                    print(resp.json())
                else:
                    print("first page attempt failed")
                    print(resp.status_code)
                    print(resp.__dir__())

        @task
        def attempt_exam_pg2(self):
            with self.client.request(
                "PUT",
                f"{host_url}/api/enrollments/exam/submit/{self.enroll_id}",
                catch_response=True,
                json={
                    "question_states": [
                        {"question": 16175, "selected_option": 64699},
                        {"question": 16176, "selected_option": 64702},
                    ],
                    "submitted": False,
                },
            ) as resp:
                if resp.status_code == 200:
                    print()
                    # save the login
                    print("second page attempt Successful")
                else:
                    print("second page attempt failed")
                    print(resp.json())

        @task
        def attempt_exam_pg3(self):
            with self.client.request(
                "PUT",
                f"{host_url}/api/enrollments/exam/submit/{self.enroll_id}",
                catch_response=True,
                json={
                    "question_states": [
                        {"question": 16177, "selected_option": 64706},
                        {"question": 16178, "selected_option": 64709},
                    ],
                    "submitted": False,
                },
            ) as resp:
                if resp.status_code == 200:
                    print("third page attempt Successful")
                    # save the login
                    # print(resp.json())
                else:
                    print("third page attempt failed")
                    print(resp.json())

        @task
        def attempt_exam_pg4(self):
            with self.client.request(
                "PUT",
                f"{host_url}/api/enrollments/exam/submit/{self.enroll_id}",
                catch_response=True,
                json={
                    "question_states": [
                        {"question": 16179, "selected_option": 64715},
                        {"question": 16180, "selected_option": 64717},
                    ],
                    "submitted": False,
                },
            ) as resp:
                if resp.status_code == 200:
                    print("fourth page attempt Successful")
                    # save the login
                    # print(resp.json())
                else:
                    print("fourth page attempt failed")
                    print(resp.json())

        @task
        def attempt_exam_pg5(self):
            with self.client.request(
                "PUT",
                f"{host_url}/api/enrollments/exam/submit/{self.enroll_id}",
                catch_response=True,
                json={
                    "question_states": [
                        {"question": 16181, "selected_option": 64722},
                        {"question": 16182, "selected_option": 64726},
                    ],
                    "submitted": True,
                },
            ) as resp:
                if resp.status_code == 200:
                    print("fifth page attempt Successful")
                    # save the login
                    # print(resp.json())
                else:
                    print("fifth page attempt failed")
                    print(resp.json())

        @task
        def wait_for_result(self):
            # wait for 10 min
            time.sleep(300)

        @task
        def get_exam_result(self):
            with self.client.request(
                "GET",
                f"{host_url}/api/enrollments/exam/result/{self.enroll_id}",
                catch_response=True,
            ) as resp:
                if resp.status_code == 200:
                    print("Exam result obtained sucessfully")
                    # save the login
                    print(resp.json())
                else:
                    print("Failed to get exam result")
                    print(resp.json())
